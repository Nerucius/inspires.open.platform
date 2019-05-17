from django import shortcuts
from django.db.models import Sum, Avg

from django.core.cache import cache
from django.http.response import HttpResponseNotFound
from django.views import View

from rest_framework.authtoken.models import Token
from backend.models import Project, Evaluation, Response, Structure

from datetime import datetime

import pandas as pd

# Constants
PHASE_TITLES = ["Phase 1", "Phase 2", "Phase 3", "Phase 4"]
QUANT = [0, 0.25, 0.50, 0.75, 1]
QUANT_TITLES = ["MIN", "Q1", "Q2", "Q3", "MAX"]


def _token_header(request):
    try:
        header_auth = request.META["HTTP_AUTHORIZATION"]
    except:
        return None
    return header_auth.split(" ")[-1]


def _token_cookie(request):
    try:
        cookies = request.META["HTTP_COOKIE"]
    except:
        return None

    cookies = [cookie.strip() for cookie in cookies.split(";")]
    for cookie in cookies:
        if "authorization" in cookie:
            return cookie.split("=")[-1]
    return None


def _authenticate_request(request, project=None):

    token = _token_header(request)
    if not token:
        token = _token_cookie(request)
    if not token:
        raise Exception("No user authentication provided")

    user = Token.objects.get(pk=token).user
    request.user = user

    if user.is_superuser:
        # Superuser can view all
        return True
    elif project and project.is_participant(user):
        # If project, only participants
        return True
    elif project is None:
        return True
    else:
        # Otherwise fuck off
        raise Exception("User can't vie this project's Evaluation")


def _get_dataframe_cache(cache_key, factory, *args, **kwargs):
    serialized_df = cache.get(cache_key)

    if serialized_df:
        # Cache hit
        dataframe = pd.read_msgpack(serialized_df)
        print("CACHE HIT: %s" % cache_key)
        return dataframe

    print("CACHE MISS: %s" % cache_key)
    # Cache miss, get dataframe using provided function and params
    dataframe = factory(*args, **kwargs)
    if dataframe is not None:
        serialized_df = dataframe.to_msgpack()
        cache.set(cache_key, serialized_df)

    return dataframe


def _get_df_responses_project(project, answer_type):
    # Filter for this project
    all_evals = Evaluation.objects.filter(phase__project=project)

    # Get only evaluations when they are marked as complete
    evals = filter(lambda x: x.is_complete, all_evals.all())
    evals = list(map(lambda x: x.id, evals))

    if len(evals) == 0:
        return None

    # Get all responses in those evals
    responses = (
        Response.objects.filter(question__answer_type=answer_type)
        .filter(evaluation__in=evals)
        .all()
    )

    # Generate data for loading into Pandas
    data = []
    index = []
    for response in responses:
        index += [response.id]
        data += [
            [
                response.question.id,
                response.evaluation.participation.project.name,
                response.question.axis,
                response.question.principle,
                response.question.dimension,
                str(response.evaluation.participation.role),
                str(response.evaluation.phase.project_phase),
                response.question.name,
                float(response.answer_degree or 0)
                if answer_type == "DEGREE"
                else "|".join([str(x.key) for x in response.answer_multiple.all()]),
            ]
        ]

    # Create pandas and calculate overall score
    df = pd.DataFrame(
        # Disabled indexing by response.id
        # index=index,
        data=data,
        columns=[
            "question",
            "project",
            "axis",
            "principle",
            "dimension",
            "role",
            "phase",
            "name",
            "response",
        ],
    )

    df = df.reset_index()
    del df["index"]
    return df


def _get_df_responses_all(answer_type):
    all_projects = Project.objects.all()

    _response_dfs = []

    for project in all_projects:
        # Get all responses from cache for given project and type
        responses = _get_dataframe_cache(
            "/v1/csv/_responses/%d/%s" % (project.id, answer_type),
            _get_df_responses_project,
            project=project,
            answer_type=answer_type,
        )
        if responses is not None:
            _response_dfs += [responses]

    all_responses = pd.concat(_response_dfs)
    all_responses = all_responses.reset_index()
    del all_responses["index"]

    return all_responses


class CSVCachedAuthorizedView(View):
    @property
    def cache_key(self):
        return self.request.META["PATH_INFO"]

    def _get_content(self, request, *args, **kwargs):
        return ""

    def get(self, request, *args, **kwargs):
        project = None
        if "project" in kwargs:
            project = Project.objects.get(pk=kwargs["project"])

        _authenticate_request(request, project)

        if self.cache_key:
            # Use cache
            content = cache.get(self.cache_key)
            if not content:
                content = self._get_content(request, *args, **kwargs)
                cache.set(self.cache_key, content, timeout=None)

        else:
            # print("WARNING: not using cache for %s" % self.request.META["PATH_INFO"])
            content = self._get_content(request, *args, **kwargs)

        return shortcuts.HttpResponse(
            content, content_type="text/plain", charset="utf8"
        )


class CSVAllResponsesMultiple(CSVCachedAuthorizedView):
    cache_key = None

    def _get_content(self, request, *args, **kwargs):
        df = _get_df_responses_all(answer_type="MULTIPLE")
        return df.to_csv()


class CSVAllResponsesDegree(CSVCachedAuthorizedView):
    cache_key = None

    def _get_content(self, request, *args, **kwargs):
        df = _get_df_responses_all(answer_type="DEGREE")
        return df.to_csv()


class CSVProjectResponsesMultiple(CSVCachedAuthorizedView):
    cache_key = None

    def _get_content(self, request, *args, **kwargs):
        ownProject = Project.objects.get(pk=kwargs["project"])
        df = _get_df_responses_project(ownProject, answer_type="MULTIPLE")
        return df.to_csv()


class CSVProjectResponsesDegree(CSVCachedAuthorizedView):
    cache_key = None

    def _get_content(self, request, *args, **kwargs):
        ownProject = Project.objects.get(pk=kwargs["project"])
        df = _get_df_responses_project(ownProject, answer_type="DEGREE")
        return df.to_csv()


class CSVProjectOverallPosition(CSVCachedAuthorizedView):
    # cache_key = None

    def _get_content(self, request, *args, **kwargs):
        ownProject = Project.objects.get(pk=kwargs["project"])

        columns = ["Project", "Evaluation", "Coherence", "Highlight"]
        data = []

        for project in Project.objects.all():
            df = _get_dataframe_cache(
                "/v1/csv/_responses/%d/DEGREE" % project.id,
                _get_df_responses_project,
                project=project,
                answer_type="DEGREE",
            )

            if df is None:
                continue

            df = df.groupby(["principle", "dimension", "phase", "role", "name"]).mean()
            df = df.groupby(["principle", "dimension", "phase", "name"]).mean()
            df = df.groupby(["principle", "dimension"]).mean()
            df = df.groupby(["principle"]).mean()

            mean = df.mean()["response"]
            coherence = (7.0 - df.std())["response"]

            data += [[project.name, mean, coherence, project == ownProject]]

        df = pd.DataFrame(columns=columns, data=data)

        return df.set_index("Project").round(2).to_csv()


class CSVProjectPhases(CSVCachedAuthorizedView):
    # cache_key = None

    def _get_content(self, request, *args, **kwargs):
        ownProject = Project.objects.get(pk=kwargs["project"])

        df_self = _get_dataframe_cache(
            "/v1/csv/_responses/%d/DEGREE" % ownProject.id,
            _get_df_responses_project,
            project=ownProject,
            answer_type="DEGREE",
        )
        df_all = _get_df_responses_all(answer_type="DEGREE")

        # Phases information
        df_p = df_self.groupby(
            ["principle", "dimension", "phase", "role", "name"]
        ).mean()
        df_p = df_p.groupby(["principle", "dimension", "phase", "name"]).mean()
        df_p = df_p.groupby(["principle", "dimension", "phase"]).mean()
        df_p = df_p.groupby(["phase"]).mean().round(2)

        # Calculate percentile for all phases
        df_pa = df_all.groupby(
            ["project", "principle", "dimension", "phase", "role", "name"]
        ).mean()
        df_pa = df_pa.groupby(
            ["project", "principle", "dimension", "phase", "name"]
        ).mean()
        df_pa = df_pa.groupby(["project", "principle", "dimension", "phase"]).mean()
        df_pa = df_pa.groupby(["project", "phase"]).mean().round(2).reset_index()

        quant_p1 = df_pa[df_pa.phase == "Phase 1"].quantile(QUANT)["response"].values
        quant_p2 = df_pa[df_pa.phase == "Phase 2"].quantile(QUANT)["response"].values
        quant_p3 = df_pa[df_pa.phase == "Phase 3"].quantile(QUANT)["response"].values
        quant_p4 = df_pa[df_pa.phase == "Phase 4"].quantile(QUANT)["response"].values

        df_quant = pd.DataFrame(
            index=PHASE_TITLES,
            columns=QUANT_TITLES,
            data=[quant_p1, quant_p2, quant_p3, quant_p4],
        )

        df = pd.DataFrame(data=df_p["response"].values, columns=["Value"])
        df["Dimension"] = PHASE_TITLES
        df["MIN"] = df_quant["MIN"].values
        df["Q1"] = df_quant["Q1"].values
        df["Q2"] = df_quant["Q2"].values
        df["Q3"] = df_quant["Q3"].values
        df["MAX"] = df_quant["MAX"].values
        df["Threshold"] = 3

        return df.set_index("Dimension").round(2).to_csv()


class CSVProjectBullets(CSVCachedAuthorizedView):
    # cache_key = None

    def _get_content(self, request, *args, **kwargs):
        ownProject = Project.objects.get(pk=kwargs["project"])

        # Load data
        df_all = _get_df_responses_all(answer_type="DEGREE")
        df_self = _get_df_responses_project(ownProject, answer_type="DEGREE")

        # Start of process
        df_all = df_all.groupby(
            ["project", "principle", "dimension", "phase", "role", "name"]
        ).mean()
        df_all = df_all.groupby(
            ["project", "principle", "dimension", "phase", "name"]
        ).mean()
        df_all_dim = df_all.groupby(["project", "principle", "dimension"]).mean()

        df_all_princ = df_all_dim.groupby(["project", "principle"]).mean()
        df_all_princ = df_all.reset_index()

        # Principle Quantiles
        princ_quant = df_all_princ.groupby(["principle"]).quantile(QUANT).reset_index()
        princ_quant["level_1"] = princ_quant.level_1.replace(QUANT, QUANT_TITLES)
        princ_quant = princ_quant.pivot_table(
            columns="level_1", values="response", index="principle"
        )
        princ_quant

        # Dimension Quantiles
        dim_quant = (
            df_all_dim.groupby(["principle", "dimension"]).quantile(QUANT).reset_index()
        )
        dim_quant["level_2"] = dim_quant.level_2.replace(QUANT, QUANT_TITLES)
        dim_quant = dim_quant.pivot_table(
            columns="level_2", values="response", index=["principle", "dimension"]
        )

        all_quant = pd.concat([princ_quant, dim_quant])

        # ========================
        #  OWN PROJECT
        # ========================
        df_self = df_self.groupby(
            ["principle", "dimension", "phase", "role", "name"]
        ).mean()
        df_self = df_self.groupby(["principle", "dimension", "phase", "name"]).mean()

        df_self_dim = df_self.groupby(["principle", "dimension"]).mean()
        df_self_princ = df_self_dim.groupby(["principle"]).mean()

        df_self = pd.concat([df_self_princ, df_self_dim])
        # df_self_princ = df_self_princ.reset_index()

        # =====================
        #  JOIN BOTH DATAFRAMES BY INDEX
        # =====================
        df_result = pd.concat([df_self, all_quant], axis=1)

        # Flatten the tuple index
        def flatten(val):
            if len(val) == 2:
                return "_".join(val)
            return val

        df_result = df_result.reset_index()
        df_result["index"] = list(map(lambda x: flatten(x), df_result["index"]))

        df_result["Indicator"] = df_result["index"].replace(
            {
                "^CITIZEN$": "Citizen-led",
                "^CITIZEN_": "Citizen",
                "ALIGNEMENT$": "Community",
                "RESPONSIVENESS$": "Responsiveness",
                "^INTEGRITY_?": "Integrity",
                "EXPECTATION$": "Expectation",
                "GENDER$": "Gender",
                "INCLUSIVITY$": "Inclusivity",
                "REFLEXIVITY$": "Reflexivity",
                "RESOURCES$": "Resource",
                "TRANSPARENCY$": "Transparency",
                "^KNOWLEDGE_?": "Knowledge",
                "OPENNESS$": "Openness",
                "RELEVANCE$": "Relevance",
                "TRANSDISCIPLINAR$": "Transdiscipl",
                "^PARTICIPATION_?": "Participatory",
                "ENGAGEMENT$": "Engagement",
                "PARTICIPATION_IMPACT$": "Impact",
                "MOTIVATION$": "Motivation",
                "SATISFACTION$": "Satisfaction",
                "^TRANSFORM_?": "Transformative",
                "COLLECTIVE$": "Collective",
                "KNOWLEDGE$": "Skills",
                "POLICY_IMPACT$": "Policy",
                "SELFIMPROVE$": "Self",
            },
            regex=True,
        )

        # Final adjustments

        def get_principle(indicator):
            if "Citizen" in indicator:
                return "Citizen-led Research"
            if "Integrity" in indicator:
                return "Integrity"
            if "Knowledge" in indicator:
                return "Knowledge Democracy"
            if "Participatory" in indicator:
                return "Participatory Dynamics"
            if "Transformative" in indicator:
                return "Transformative Change"
            return "NOT FOUND"

        df_result["Principle"] = list(
            map(lambda x: get_principle(x), df_result["Indicator"])
        )

        df_result["AbsValue"] = df_result["response"]
        df_result = df_result[["Principle", "Indicator", "AbsValue"] + QUANT_TITLES]
        df_result["Threshold"] = 3

        df_result = df_result.set_index(["Principle", "Indicator"])

        return df_result.round(2).to_csv()


class CSVStructureSummaryExport(CSVCachedAuthorizedView):
    cache_key = None

    def _get_content(self, request, *args, **kwargs):
        structure_pk = kwargs["structure"]
        structure = Structure.objects.get(pk=structure_pk)

        if not structure.can_write(request.user):
            raise Exception("403 forbidden")

        export = []

        for collab in structure.collaborations.all():
            project = collab.project

            for part in project.participation_set.all():

                role_name = part.role.name.split(".")[-1]

                line = [
                    structure.name,
                    project.name,
                    role_name,
                    part.user.full_name,
                    datetime.isoformat(part.created_at.replace(microsecond=0)),
                ]
                export += [",".join(line)]

        headers = ",".join(["Structure", "Project", "Role", "User", "Date Joined"])
        return "\n".join([headers] + export)


class CSVProjectSummaryExport(CSVCachedAuthorizedView):
    cache_key = None

    def _get_content(self, request, *args, **kwargs):
        project_pk = kwargs["project"]
        project = Project.objects.get(pk=project_pk)

        if not project.can_write(request.user):
            raise Exception("403 forbidden")

        export = []

        for part in project.participation_set.all():
            role_name = part.role.name.split(".")[-1]
            line = [project.name, role_name, part.user.full_name]
            export += [",".join(line)]

        headers = ",".join(["Project", "Role", "User"])
        return "\n".join([headers] + export)


# =========================================
#  FUNCTION BASED VIEWS
# =========================================


def csv_tangram(request, project):
    """
        Public evaluation results
        ```
        citizen,    integrity,  knowledge,  participation,  transform
        2,          4,          2,          2,              4
        ```
    """
    ownProject = Project.objects.get(pk=project)
    _authenticate_request(request, project=None)

    df_all = _get_df_responses_all(answer_type="DEGREE")
    df_self = _get_dataframe_cache(
        "/v1/csv/_responses/%d/DEGREE" % ownProject.id,
        _get_df_responses_project,
        project=ownProject,
        answer_type="DEGREE",
    )

    if df_self is None:
        return HttpResponseNotFound("Project not yet evaluated")

    df_all = df_all.groupby(
        ["project", "principle", "dimension", "phase", "role", "name"]
    ).mean()
    df_all = df_all.groupby(
        ["project", "principle", "dimension", "phase", "name"]
    ).mean()
    df_all = df_all.groupby(["project", "principle", "dimension"]).mean()
    df_all = df_all.groupby(["project", "principle"]).mean()
    df_all = df_all.groupby(["principle"]).quantile(QUANT)
    df_all = df_all.reset_index()
    df_all = df_all.pivot_table(columns="level_1", values="response", index="principle")
    df_all.columns = QUANT_TITLES

    # Calculate where
    df_self = df_self.groupby(
        ["principle", "dimension", "phase", "role", "name"]
    ).mean()
    df_self = df_self.groupby(["principle", "dimension", "phase", "name"]).mean()
    df_self = df_self.groupby(["principle", "dimension"]).mean()
    df_self = df_self.groupby(["principle"]).mean()
    df_self.columns = ["value"]

    df_all["Quartile"] = 1
    df_all["Quartile"] = df_all["Quartile"] + (df_self.value > df_all.Q1) * 1
    df_all["Quartile"] = df_all["Quartile"] + (df_self.value > df_all.Q2) * 1
    df_all["Quartile"] = df_all["Quartile"] + (df_self.value > df_all.Q3) * 1

    df_all = df_all.pivot_table(values="Quartile", columns="principle")
    df_all.columns = ["citizen", "integrity", "knowledge", "participation", "transform"]
    df_all = df_all.reset_index()
    del df_all["index"]

    return shortcuts.HttpResponse(df_all.to_csv(), content_type="text/plain")


def csv_heatmap(request, project):
    ownProject = Project.objects.get(pk=project)
    _authenticate_request(request, ownProject)

    return shortcuts.HttpResponse(
        """
        Principle,Dimension,Indicator,Value
        1,1. Search for a topic,AG1Stage1,3.00
        1,2. Formulation of research question,AG1Stage2,4.00
        1,3. Method design,AG1Stage3,3.00
        1,4. Data collection,AG1Stage4,4.00
        1,5. Data analysis and interpretation,AG1Stage5,2.00
        1,6. Publication of the results,AG1Stage6,2.00
        1,7. Public awareness,AG1Stage7,3.00
        1,8. Project governance,AG1Stage8,0.00
        1,9. Transformative change,AG1Stage9,2.00
        2,1. Search for a topic,AG2Stage1,2.00
        2,2. Formulation of research question,AG2Stage2,4.00
        2,3. Method design,AG2Stage3,4.00
        2,4. Data collection,AG2Stage4,2.00
        2,5. Data analysis and interpretation,AG2Stage5,0.00
        2,6. Publication of the results,AG2Stage6,0.00
        2,7. Public awareness,AG2Stage7,0.00
        2,8. Project governance,AG2Stage8,0.00
        2,9. Transformative change,AG2Stage9,0.00
        """,
        content_type="text/plain",
    )

