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

CSV_LINE_SEPARATOR = "\n"
CSV_COLUMN_SEPARATOR = "|"


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
        # No project requested, continue
        return True
    else:
        # Otherwise fuck off
        raise Exception("403 Forbidden")


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


def _newline_to_br(text):
    return text.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br/> ")


def _structures_to_csv_lines(structures):
    lines = []
    for structure in structures:
        knowledge_areas = ";".join(
            [ka.name.split(".")[-1].upper() for ka in structure.knowledge_areas.all()]
        )

        line = [
            str(structure.id),
            structure.name,
            structure.structure_type,
            structure.country_code,
            _newline_to_br(structure.summary),
            _newline_to_br(structure.description),
            knowledge_areas,
        ]
        lines += [CSV_COLUMN_SEPARATOR.join(line)]

    headers = CSV_COLUMN_SEPARATOR.join(
        [
            "id",
            "name",
            "structure_type",
            "country_code",
            "summary",
            "description",
            "knowledge_areas",
        ]
    )
    return CSV_LINE_SEPARATOR.join([headers] + lines)


def _projects_to_csv_lines(projects):
    lines = []
    for project in projects:

        knowledge_area = (
            project.knowledge_area.name.split(".")[-1].upper()
            if project.knowledge_area
            else ""
        )
        pap = project.phases.filter(projectatphase__is_active=True).first()
        project_phase = str(pap) if pap else ""
        participants = ";".join(
            [
                "%s (%s)" % (p.user.full_name, str(p.role).replace(" ", "").upper())
                for p in project.participation_set.all()
            ]
        )

        line = [
            str(project.structure.id) if project.structure else "",
            project.structure.name if project.structure else "",
            str(project.id),
            project.name,
            project.project_type,
            knowledge_area,
            project.country_code,
            _newline_to_br(project.summary),
            _newline_to_br(project.description),
            project_phase,
            project.contact_website,
            participants,
        ]
        lines += [CSV_COLUMN_SEPARATOR.join(line)]

    headers = CSV_COLUMN_SEPARATOR.join(
        [
            "structure_id",
            "structure",
            "id",
            "name",
            "project_type",
            "knowledge_area",
            "country_code",
            "summary",
            "description",
            "current_phase",
            "contact_website",
            "participants",
        ]
    )
    return CSV_LINE_SEPARATOR.join([headers] + lines)


class CSVCachedAuthorizedView(View):
    @property
    def cache_key(self):
        return self.request.META["PATH_INFO"]

    def _get_content(self, request, *args, **kwargs):
        return ""

    def _get_content_wrapper(self, request, *args, **kwargs):
        try:
            return self._get_content(request, *args, **kwargs)
        except Exception:
            return ""

    def get(self, request, *args, **kwargs):
        project = None
        if "project" in kwargs:
            project = Project.objects.get(pk=kwargs["project"])

        _authenticate_request(request, project)

        # Use cache
        if self.cache_key:
            content = cache.get(self.cache_key)
            if not content:
                content = self._get_content(request, *args, **kwargs)
                cache.set(self.cache_key, content, timeout=None)
        else:
            content = self._get_content(request, *args, **kwargs)
            cache.set(self.cache_key, content, timeout=None)

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
    cache_key = None

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
    cache_key = None

    def _get_content(self, request, *args, **kwargs):
        ownProject = Project.objects.get(pk=kwargs["project"])

        df_self = _get_dataframe_cache(
            "/v1/csv/_responses/%d/DEGREE" % ownProject.id,
            _get_df_responses_project,
            project=ownProject,
            answer_type="DEGREE",
        )
        df_all = _get_df_responses_all(answer_type="DEGREE")

        PHASE_TITLES = ["Phase 1", "Phase 2", "Phase 3", "Phase 4"]
        QUANT = [0, 0.25, 0.50, 0.75, 1]
        QUANT_TITLES = ["MIN", "Q1", "Q2", "Q3", "MAX"]

        # Group by all projects all phases
        df_pa = df_all.groupby(
            ["project", "principle", "dimension", "phase", "role", "name"]
        ).mean()
        df_pa = df_pa.groupby(
            ["project", "principle", "dimension", "phase", "name"]
        ).mean()
        df_pa = df_pa.groupby(["project", "principle", "dimension", "phase"]).mean()
        df_pa = df_pa.groupby(["project", "phase"]).mean()
        df_pa = df_pa.reset_index()

        # Calculate each phase percentile according to all projects
        quant_p1 = df_pa[df_pa.phase == "Phase 1"].quantile(QUANT)["response"].values
        quant_p2 = df_pa[df_pa.phase == "Phase 2"].quantile(QUANT)["response"].values
        quant_p3 = df_pa[df_pa.phase == "Phase 3"].quantile(QUANT)["response"].values
        quant_p4 = df_pa[df_pa.phase == "Phase 4"].quantile(QUANT)["response"].values
        # Join all info into single dataframe
        df_qa = pd.DataFrame(
            index=PHASE_TITLES,
            columns=QUANT_TITLES,
            data=[quant_p1, quant_p2, quant_p3, quant_p4],
        )
        df_qa.index.name = "phase"

        # Calculate self value
        df_ps = df_self.groupby(
            ["principle", "dimension", "phase", "role", "name"]
        ).mean()
        df_ps = df_ps.groupby(["principle", "dimension", "phase", "name"]).mean()
        df_ps = df_ps.groupby(["principle", "dimension", "phase"]).mean()
        df_ps = df_ps.groupby(["phase"]).mean()

        # Create result by concatenation
        df_result = df_qa
        df_result["Value"] = df_ps
        df_result["Principle"] = "General"
        df_result["Threshold"] = 3.0
        df_result["Dimension"] = ["Phase1", "Phase2", "Phase3", "Phase4"]

        df_result = df_result[
            ["Principle", "Dimension", "Value", *QUANT_TITLES, "Threshold"]
        ]

        return df_result.fillna(0).round(2).to_csv(index=False)


class CSVProjectHeatmap(CSVCachedAuthorizedView):
    cache_key = None

    def _get_content(self, request, *args, **kwargs):
        ownProject = Project.objects.get(pk=kwargs["project"])

        df_self = _get_dataframe_cache(
            "/v1/csv/_responses/%d/MULTIPLE" % ownProject.id,
            _get_df_responses_project,
            project=ownProject,
            answer_type="MULTIPLE",
        )

        df = df_self

        df["response"] = df["response"].fillna("")
        for key in "123456789":
            df["multi_%s" % key] = df["response"].str.contains(key) * 1

        df = df.groupby(["role", "dimension", "principle"]).mean()
        df = df.groupby(["dimension", "principle"]).sum().round()

        df = df.transpose()
        df = df.stack()
        df = df.reset_index().sort_values(["principle"])
        df.fillna(0, inplace=True)

        df = df.replace("multi_1", "1. Search for a topic")
        df = df.replace("multi_2", "2. Formulation of research question")
        df = df.replace("multi_3", "3. Method design")
        df = df.replace("multi_4", "4. Data collection")
        df = df.replace("multi_5", "5. Data analysis and interpretation")
        df = df.replace("multi_6", "6. Publication of the results")
        df = df.replace("multi_7", "7. Public awareness")
        df = df.replace("multi_8", "8. Project governance")
        df = df.replace("multi_9", "9. Transformative change")

        df["Value"] = 0
        try:
            df["Value"] += df.ENGAGEMENT
        except Exception:
            pass
        try:
            df["Value"] += df.RESPONSIVENESS
        except Exception:
            pass

        df = df[["principle", "level_0", "Value"]]
        df.columns = ["Principle", "Dimension", "Value"]
        df = df.replace({"CITIZEN": 1, "PARTICIPATION": 2})
        df_result = df

        return df_result.to_csv(index=False)


class CSVProjectBulletPrinciples(CSVCachedAuthorizedView):
    cache_key = None

    def _get_content(self, request, *args, **kwargs):
        ownProject = Project.objects.get(pk=kwargs["project"])

        # Load data
        df_all = _get_df_responses_all(answer_type="DEGREE")
        df_self = _get_df_responses_project(ownProject, answer_type="DEGREE")

        # Reduce to principle from role -> name -> dimension -> principle
        df_all = df_all.groupby(
            ["project", "principle", "dimension", "phase", "role", "name"]
        ).mean()
        df_all = df_all.groupby(
            ["project", "principle", "dimension", "phase", "name"]
        ).mean()
        df_all_dim = df_all.groupby(["project", "principle", "dimension"]).mean()
        df_all_princ = df_all_dim.groupby(["project", "principle"]).mean()

        # For each specified quantile level, get value.
        _tmp = []
        _tmp2 = df_all_princ.groupby("principle")
        for i, q in enumerate(QUANT_TITLES):
            df_quantile = _tmp2.quantile(QUANT[i])
            df_quantile.columns = [q]
            _tmp += [df_quantile]

        # Concatenate results
        all_princ_quant = pd.concat(_tmp, axis=1)

        # Calculate this project's values
        df_self = df_self.groupby(
            ["principle", "dimension", "phase", "role", "name"]
        ).mean()
        df_self = df_self.groupby(["principle", "dimension", "phase", "name"]).mean()
        df_self_dim = df_self.groupby(["principle", "dimension"]).mean()
        df_self_princ = df_self_dim.groupby(["principle"]).mean()

        df_self = df_self_princ
        df_self.columns = ["AbsValue"]

        df_result = pd.concat([df_self, all_princ_quant], axis=1)
        df_result = df_result.sort_index().reset_index()
        df_result["Threshold"] = 3
        df_result["Dimension"] = "Total"
        df_result["Indicator"] = [
            "Citizen-led",
            "Integrity",
            "Knowledge",
            "Participatory",
            "Transformative",
        ]
        df_result["Principle"] = [
            "Citizen-led Research",
            "Integrity",
            "Knowledge Democracy",
            "Participatory Dynamics",
            "Transformative Change",
        ]
        df_result = df_result[
            [
                "Principle",
                "Dimension",
                "Indicator",
                "AbsValue",
                *QUANT_TITLES,
                "Threshold",
            ]
        ]

        return df_result.round(2).to_csv(index=False)


class CSVProjectBulletDimensions(CSVCachedAuthorizedView):
    cache_key = None

    def _get_content(self, request, *args, **kwargs):
        ownProject = Project.objects.get(pk=kwargs["project"])

        # Load data
        df_all = _get_df_responses_all(answer_type="DEGREE")
        df_self = _get_df_responses_project(ownProject, answer_type="DEGREE")

        # Start of process
        # Reduce to (principle, role)
        df_all = df_all.groupby(
            ["project", "principle", "dimension", "phase", "role", "name"]
        ).mean()
        df_all_dim = df_all.groupby(
            ["project", "principle", "dimension", "role"]
        ).mean()
        df_all_dim = df_all_dim.groupby(["project", "principle", "dimension"]).mean()

        # For each specified quantile level, get value.
        _tmp = []
        _tmp2 = df_all_dim.groupby(["principle", "dimension"])
        for i, q in enumerate(QUANT_TITLES):
            df_quantile = _tmp2.quantile(QUANT[i])
            df_quantile.columns = [q]
            _tmp += [df_quantile]

        # Concatenate results
        all_dim_quant = pd.concat(_tmp, axis=1)

        # # Calculate this project's values
        df_self = df_self.groupby(
            ["principle", "dimension", "phase", "role", "name"]
        ).mean()
        df_self = df_self.groupby(["principle", "dimension", "phase", "role"]).mean()
        df_self = df_self.groupby(["principle", "dimension", "role"]).mean()
        df_self = df_self.groupby(["principle", "dimension"]).mean()
        df_self.columns = ["AbsValue"]

        # # Build resulting dataframe
        df_result = pd.concat([df_self, all_dim_quant], axis=1)
        df_result = df_result.sort_index().reset_index()
        df_result["Threshold"] = 3
        df_result["Principle"] = df_result.principle.replace(
            {
                "CITIZEN": "Citizen-led Research",
                "INTEGRITY": "Integrity",
                "KNOWLEDGE": "Knowledge Democracy",
                "PARTICIPATION": "Participatory Dynamics",
                "TRANSFORM": "Transformative Change",
            }
        )
        del df_result["principle"]
        df_result["Dimension"] = df_result.dimension.replace(
            {
                "ALIGNEMENT": "Community alignment",
                "RESPONSIVENESS": "Responsiveness to community alignment",
                "EXPECTATION": "Expectation alignment",
                "GENDER": "Gender perspective",
                "INCLUSIVITY": "Inclusivity",
                "REFLEXIVITY": "Reflexivity",
                "RESOURCES": "Resource availability",
                "TRANSPARENCY": "Transparency",
                "OPENNESS": "Openness",
                "RELEVANCE": "Scientific relevance",
                "TRANSDISCIPLINAR": "Transdisciplinarity",
                "ENGAGEMENT": "Degree of engagement",
                "MOTIVATION": "Impact of the participatory dynamics",
                "PARTICIPATION_IMPACT": "Motivation",
                "SATISFACTION": "Satisfaction with the participatory dynamics",
                "COLLECTIVE": "Collective capacity",
                "KNOWLEDGE": "Knowledge and skills",
                "POLICY_IMPACT": "Policy impact",
                "SELFIMPROVE": "Self-improvement",
            }
        )
        del df_result["dimension"]
        df_result

        def to_indicator(it):
            row = it[1]
            return (
                row["Principle"].split()[0].split("-")[0]
                + row["Dimension"].split()[0].split("-")[0]
            )

        df_result["Indicator"] = list(map(to_indicator, df_result.iterrows()))

        # Final fixes to names
        df_result.Indicator.replace(
            {
                "TransformativeKnowledge": "TransformativeSkills",
                "ParticipatoryDegree": "ParticipatoryEngagement",
                "KnowledgeScientific": "KnowledgeRelevance",
                "KnowledgeTransdisciplinarity": "KnowledgeTransdiscipl",
            },
            inplace=True,
        )

        # Reorder columns
        df_result = df_result[
            [
                "Principle",
                "Dimension",
                "Indicator",
                "AbsValue",
                *QUANT_TITLES,
                "Threshold",
            ]
        ]

        return df_result.round(2).to_csv(index=False)


class CSVProjectBulletRoles(CSVCachedAuthorizedView):
    cache_key = None

    def _get_content(self, request, *args, **kwargs):
        ownProject = Project.objects.get(pk=kwargs["project"])

        # Load data
        df_all = _get_df_responses_all(answer_type="DEGREE")
        df_self = _get_df_responses_project(ownProject, answer_type="DEGREE")

        # Start of process
        # Reduce to (principle, role)
        df_all = df_all.groupby(
            ["project", "principle", "dimension", "phase", "role", "name"]
        ).mean()
        df_all_dim = df_all.groupby(
            ["project", "principle", "dimension", "role"]
        ).mean()
        df_all_role = df_all_dim.groupby(["project", "principle", "role"]).mean()

        # For each specified quantile level, get value.
        _tmp = []
        _tmp2 = df_all_role.groupby(["principle", "role"])
        for i, q in enumerate(QUANT_TITLES):
            df_quantile = _tmp2.quantile(QUANT[i])
            df_quantile.columns = [q]
            _tmp += [df_quantile]

        # Concatenate results
        all_role_quant = pd.concat(_tmp, axis=1)

        # Calculate this project's values
        df_self = df_self.groupby(
            ["principle", "dimension", "phase", "role", "name"]
        ).mean()
        df_self = df_self.groupby(["principle", "dimension", "phase", "role"]).mean()
        df_self_dim = df_self.groupby(["principle", "dimension", "role"]).mean()
        df_self_princ = df_self_dim.groupby(["principle", "role"]).mean()

        df_self = df_self_princ
        df_self.columns = ["AbsValue"]

        # Build resulting dataframe
        df_result = pd.concat([df_self, all_role_quant], axis=1)
        df_result = df_result.sort_index().reset_index()
        df_result["Threshold"] = 3
        df_result["Dimension"] = df_result["role"]
        df_result["Principle"] = df_result["principle"]
        del df_result["role"]
        del df_result["principle"]

        df_result.replace(
            {
                "CITIZEN": "Citizen-led Research",
                "INTEGRITY": "Integrity",
                "KNOWLEDGE": "Knowledge Democracy",
                "PARTICIPATION": "Participatory Dynamics",
                "TRANSFORM": "Transformative Change",
            },
            inplace=True,
        )

        def to_indicator(it):
            row = it[1]
            return (
                row["Principle"].split()[0].split("-")[0]
                + row["Dimension"].split()[0][:12]
            )

        df_result["Indicator"] = list(map(to_indicator, df_result.iterrows()))
        df_result = df_result[
            [
                "Principle",
                "Dimension",
                "Indicator",
                "AbsValue",
                *QUANT_TITLES,
                "Threshold",
            ]
        ]

        return df_result.round(2).to_csv(index=False)


class CSVStructureSummaryExport(CSVCachedAuthorizedView):
    cache_key = None

    def _get_content(self, request, *args, **kwargs):
        structure_pk = kwargs["structure"]
        structure = Structure.objects.get(pk=structure_pk)

        if not structure.can_write(request.user):
            raise Exception("403 No access to structure")

        export = []

        for collab in structure.collaborations.all():
            project = collab.project

            for part in project.participation_set.all():
                role_name = part.role.name.split(".")[-1].upper()

                line = [
                    str(structure.id),
                    structure.name,
                    str(project.id),
                    project.name,
                    role_name,
                    part.user.full_name,
                    part.user.email,
                    datetime.isoformat(part.created_at.replace(microsecond=0)),
                ]
                export += [CSV_COLUMN_SEPARATOR.join(line)]

        headers = CSV_COLUMN_SEPARATOR.join(
            [
                "structure_id",
                "structure_name",
                "project_id",
                "project_name",
                "user_role",
                "user_name",
                "user_email",
                "user_date_joined",
            ]
        )
        return CSV_LINE_SEPARATOR.join([headers] + export)


class CSVProjectSummaryExport(CSVCachedAuthorizedView):
    cache_key = None

    def _get_content(self, request, *args, **kwargs):
        project_pk = kwargs["project"]
        project = Project.objects.get(pk=project_pk)

        if not project.can_write(request.user):
            raise Exception("403 no access to project")

        export = []

        for part in project.participation_set.all():
            role_name = part.role.name.split(".")[-1].upper()
            line = [
                str(project.structure.id) if project.structure else "",
                project.structure.name if project.structure else "",
                str(project.id),
                project.name,
                role_name,
                part.user.full_name,
                part.user.email,
                datetime.isoformat(part.created_at.replace(microsecond=0)),
            ]
            export += [CSV_COLUMN_SEPARATOR.join(line)]

        headers = CSV_COLUMN_SEPARATOR.join(
            [
                "structure_id",
                "structure_name",
                "project_id",
                "project_name",
                "user_role",
                "user_name",
                "user_email",
                "user_date_joined",
            ]
        )
        return CSV_LINE_SEPARATOR.join([headers] + export)


class CSVAllOwnProjectsExport(CSVCachedAuthorizedView):
    cache_key = None

    def _get_content(self, request, *args, **kwargs):
        user = request.user
        all_projects = user.owned_projects.all()
        all_projects |= user.managed_projects.all()
        all_projects |= user.researched_projects.all()
        all_projects = set(all_projects)

        return _projects_to_csv_lines(all_projects)


class CSVAllOwnStructresExport(CSVCachedAuthorizedView):
    cache_key = None

    def _get_content(self, request, *args, **kwargs):
        user = request.user
        all_structures = user.owned_structures.all()
        all_structures |= user.managed_structures.all()
        all_structures = set(all_structures)

        return _structures_to_csv_lines(all_structures)


class CSVAdminAllProjects(CSVCachedAuthorizedView):
    cache_key = None

    def _get_content(self, request, *args, **kwargs):
        if not request.user.is_administrator:
            raise Exception("Must be administrator")

        all_projects = Project.objects.all()
        return _projects_to_csv_lines(all_projects)


class CSVAdminAllStructures(CSVCachedAuthorizedView):
    cache_key = None

    def _get_content(self, request, *args, **kwargs):
        if not request.user.is_administrator:
            raise Exception("Must be administrator")

        all_structures = Structure.objects.all()
        return _structures_to_csv_lines(all_structures)


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
