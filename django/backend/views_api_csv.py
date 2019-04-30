from django import shortcuts
from django.db.models import Sum, Avg

from django.core.cache import cache
from django.views import View

from rest_framework.authtoken.models import Token
from backend.models import Project, Evaluation, Response

import pandas as pd


def _authenticate_request(request, project=None):
    try:
        cookies = request.META["HTTP_COOKIE"]
    except:
        raise Exception("No authentication provided in request")

    cookies = [x.strip() for x in cookies.split(";")]
    cookies = dict([cookie.split("=") for cookie in cookies])

    if "authorization" in cookies:
        # Get user given the provided token
        token = cookies["authorization"]
        user = Token.objects.get(pk=token).user

        if user.is_superuser:
            # Superuser can view all
            return True
        elif project and project.is_participant(user):
            # If project, only participants
            return True
        else:
            # Otherwise fuck off
            raise Exception("User can't vie this project's Evaluation")

    else:
        # No auth provided
        raise Exception("No authentication provided in request")


def _dataframe_response(df, index=False):
    return shortcuts.HttpResponse(
        df.to_csv(index=index), content_type="text/plain", charset="utf8"
    )


def _get_dataframe_all_responses(project=None, answer_type="DEGREE"):
    # Get evaluations for this project which are complete
    all_evals = Evaluation.objects
    if project:
        all_evals = Evaluation.objects.filter(phase__project=project)
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
        index=index,
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

    return df


class CSVCachedAuthorizedView(View):
    @property
    def cache_key(self):
        return self.request.META["PATH_INFO"]

    def _get_content(self, request, *args, **kwargs):
        return ""

    def get(self, request, *args, **kwargs):
        if "project" in kwargs:
            project = Project.objects.get(pk=kwargs["project"])

        _authenticate_request(request, project or None)

        content = cache.get(self.cache_key)
        if not content:
            content = self._get_content(request, *args, **kwargs)
            cache.set(self.cache_key, content, timeout=None)

        return shortcuts.HttpResponse(
            content, content_type="text/plain", charset="utf8"
        )


class CSVAllResponsesMultiple(CSVCachedAuthorizedView):
    def _get_content(self, request, *args, **kwargs):
        df = _get_dataframe_all_responses(answer_type="MULTIPLE")
        return df.to_csv()


class CSVAllResponsesDegree(CSVCachedAuthorizedView):
    def _get_content(self, request, *args, **kwargs):
        df = _get_dataframe_all_responses(answer_type="DEGREE")
        return df.to_csv()


class CSVProjectResponsesMultiple(CSVCachedAuthorizedView):
    def _get_content(self, request, *args, **kwargs):
        ownProject = Project.objects.get(pk=kwargs["project"])
        df = _get_dataframe_all_responses(ownProject, answer_type="MULTIPLE")
        return df.to_csv()


class CSVProjectResponsesDegree(CSVCachedAuthorizedView):
    def _get_content(self, request, *args, **kwargs):
        ownProject = Project.objects.get(pk=kwargs["project"])
        df = _get_dataframe_all_responses(ownProject, answer_type="DEGREE")
        return df.to_csv()


class CSVProjectOverallPosition(CSVCachedAuthorizedView):
    def _get_content(self, request, *args, **kwargs):
        ownProject = Project.objects.get(pk=kwargs["project"])

        columns = ["Project", "Evaluation", "Coherence", "Highlight"]
        data = []

        for project in Project.objects.all():
            df = _get_dataframe_all_responses(project)
            if df is None:
                continue

            df = df.groupby(["principle", "phase", "role", "name"]).mean()
            df = df.groupby(["principle"]).mean()

            mean = df.mean().round(2)["response"]
            coherence = (1.0 / df.std()).round(2)["response"]

            data += [[project.name, mean, coherence, project == ownProject]]
        df = pd.DataFrame(columns=columns, data=data)

        return df.to_csv()


class CSVProjectPhases(CSVCachedAuthorizedView):
    def _get_content(self, request, *args, **kwargs):
        ownProject = Project.objects.get(pk=kwargs["project"])

        df = _get_dataframe_all_responses(ownProject)

        df = df.groupby(["phase", "role", "name"]).mean()
        df = df.groupby(["phase"]).mean().round(2)

        print(df["response"].values)

        df = pd.DataFrame(data=df["response"].values, columns=["Value"])
        df["Dimension"] = ["Phase 1", "Phase 2", "Phase 3", "Phase 4"]
        df["MIN"] = 2
        df["Q1"] = 2.5
        df["Q2"] = 3.5
        df["Q3"] = 5
        df["MAX"] = 6
        df["Threshold"] = 3

        return df.to_csv()


# =========================================
#  FUNCTION BASED VIEWS
# =========================================


def csv_bullets(request, project):
    ownProject = Project.objects.get(pk=project)
    _authenticate_request(request, ownProject)

    # ownProject = Project.objects.get(pk=project)

    # df = _get_dataframe_all_responses(ownProject)

    # df = df.groupby(["principle", "dimension", "phase", "role", "name"]).mean()
    # # Perform different groupings
    # df_principle = df.groupby(["principle"]).mean().reset_index()
    # df_dimension = df.groupby(["principle", "dimension"]).mean().reset_index()
    # df_role = df.groupby(["principle", "role"]).mean().reset_index()

    # # Add column to mark "aggregated by all"
    # df_principle["role"] = "All"
    # df_principle["dimension"] = "All"
    # df_dimension["role"] = "All"
    # df_role["dimension"] = "All"

    # df = pd.concat([df_principle, df_dimension, df_role])[
    #     ["principle", "dimension", "role", "response"]
    # ]
    # df.columns = ["Principle", "Dimension", "Indicator", "AbsValue"]

    # df["MIN"] = 1
    # df["Q1"] = 2.5
    # df["Q2"] = 3.5
    # df["Q3"] = 5
    # df["MAX"] = 6
    # df["Threshold"] = 3

    # df.replace("CITIZEN", "Citizen-led Research", inplace=True)
    # df.replace("INTEGRITY", "Integrity", inplace=True)
    # df.replace("KNOWLEDGE", "Knowledge Democracy", inplace=True)
    # df.replace("PARTICIPATION", "Participatory Dynamics", inplace=True)
    # df.replace("TRANSFORM", "Transformative Change", inplace=True)

    # df.replace("ALIGNEMENT", "Community alignment", inplace=True)
    # df.replace("RESPONSIVENESS", "Responsiveness to community alignment", inplace=True)

    return shortcuts.HttpResponse(
        """Principle,Dimension,Indicator,AbsValue,MIN,Q1,Q2,Q3,MAX,Threshold,RelValue,Color
Citizen-led Research,Community alignment,CitizenCommunity,4.07,4.07,4.20,4.30,4.95,6.13,3.00,1,#00796B
Citizen-led Research,Responsiveness to community alignment,CitizenResponsiveness,4.50,3.42,3.75,4.50,5.00,6.00,3.00,3,#00796B
Citizen-led Research,Total,Citizen-led,4.23,4.03,4.23,4.38,4.56,6.08,3.00,2,#00796B
Citizen-led Research,Civil Society,CitizenCivil,4.14,3.71,4.14,4.29,4.43,6.14,3.00,2,#00796B
Citizen-led Research,Project Manager,CitizenProject,5.33,3.33,4.67,5.33,5.67,6.33,3.00,3,#00796B
Citizen-led Research,Scientist,CitizenScientist,3.67,3.67,4.00,5.00,5.33,5.33,3.00,1,#00796B
Citizen-led Research,Student,CitizenStudent,4.67,3.00,3.00,4.00,4.67,6.00,3.00,4,#00796B
Integrity,Expectation alignment,IntegrityExpectation,4.50,3.88,4.13,4.50,4.50,4.75,3.00,4,#F17600
Integrity,Gender perspective,IntegrityGender,3.00,3.00,3.00,3.75,3.75,4.25,3.00,2,#F17600
Integrity,Inclusivity,IntegrityInclusivity,6.33,0.00,5.00,5.50,5.83,6.33,3.00,4,#F17600
Integrity,Reflexivity,IntegrityReflexivity,0.00,0.00,0.00,0.00,0.00,4.00,3.00,4,#F17600
Integrity,Resource availability,IntegrityResource,5.00,4.00,4.67,5.00,5.33,5.67,3.00,3,#F17600
Integrity,Transparency,IntegrityTransparency,4.00,1.00,1.50,4.00,4.00,6.00,3.00,4,#F17600
Integrity,Total,Integrity,3.90,3.44,3.48,3.63,3.90,3.96,3.00,4,#F17600
Integrity,Civil Society,IntegrityCivil,4.33,2.67,3.00,4.33,4.67,5.33,3.00,3,#F17600
Integrity,Project Manager,IntegrityProject,4.00,3.58,3.75,3.75,3.83,4.00,3.00,4,#F17600
Integrity,Scientist,IntegrityScientist,4.00,3.33,3.67,4.00,4.00,4.33,3.00,4,#F17600
Integrity,Student,IntegrityStudent,5.00,2.50,4.00,4.00,5.00,6.00,3.00,4,#F17600
Knowledge Democracy,Openness,KnowledgeOpenness,5.75,4.00,5.25,5.75,5.75,6.25,3.00,4,#2599D4
Knowledge Democracy,Scientific relevance,KnowledgeRelevance,3.22,2.44,3.22,4.22,5.00,6.33,3.00,2,#2599D4
Knowledge Democracy,Transdisciplinarity,KnowledgeTransdiscipl,5.88,3.88,5.00,5.75,5.88,5.88,3.00,4,#2599D4
Knowledge Democracy,Total,Knowledge,4.70,3.30,4.70,5.07,5.10,6.18,3.00,2,#2599D4
Knowledge Democracy,Civil Society,KnowledgeCivil,5.50,4.00,5.00,5.50,5.50,6.00,3.00,4,#2599D4
Knowledge Democracy,Project Manager,KnowledgeProject,5.40,4.00,5.40,5.40,5.40,6.20,3.00,4,#2599D4
Knowledge Democracy,Scientist,KnowledgeScientist,4.00,3.00,4.00,4.50,5.25,6.50,3.00,2,#2599D4
Knowledge Democracy,Student,KnowledgeStudent,4.50,4.00,4.50,4.50,5.00,5.50,3.00,3,#2599D4
Participatory Dynamics,Degree of engagement,ParticipatoryEngagement,6.00,5.00,5.00,6.00,7.00,7.00,3.00,3,#DAE14B
Participatory Dynamics,Impact of the participatory dynamics,ParticipatoryImpact,4.00,2.50,4.00,4.00,4.00,5.00,3.00,4,#DAE14B
Participatory Dynamics,Motivation,ParticipatoryMotivation,5.22,3.39,5.19,5.22,5.36,5.97,3.00,3,#DAE14B
Participatory Dynamics,Satisfaction with the participatory dunamics,ParticipatorySatisfaction,2.67,2.67,3.17,3.83,4.67,5.17,3.00,1,#DAE14B
Participatory Dynamics,Total,Participatory,4.19,3.63,4.19,4.40,4.95,5.38,3.00,2,#DAE14B
Participatory Dynamics,Civil Society,ParticipatoryCivil,5.17,4.00,4.17,5.00,5.17,5.50,3.00,4,#DAE14B
Participatory Dynamics,Project Manager,ParticipatoryProject,3.00,2.25,3.00,4.25,5.50,5.50,3.00,2,#DAE14B
Participatory Dynamics,Scientist,ParticipatoryScientist,3.80,2.40,3.80,4.20,5.00,5.20,3.00,2,#DAE14B
Participatory Dynamics,Student,ParticipatoryStudent,5.00,2.25,4.75,5.00,5.25,6.00,3.00,3,#DAE14B
Transformative Change,Collective capacity,TransformativeCollective,4.83,3.33,3.83,4.83,4.83,5.33,3.00,4,#2F4193
Transformative Change,Knowledge and skills,TransformativeSkills,4.75,3.00,3.75,4.25,4.75,5.75,3.00,4,#2F4193
Transformative Change,Policy impact,TransformativePolicy,5.17,0.00,0.00,2.83,5.17,6.50,3.00,4,#2F4193
Transformative Change,Self-improvement,TransformativeSelf,4.88,1.88,3.00,3.38,4.88,5.50,3.00,4,#2F4193
Transformative Change,Total,Transformative,4.88,2.85,3.14,3.15,4.88,5.47,3.00,4,#2F4193
Transformative Change,Civil Society,TransformativeCivil,5.29,1.29,2.00,3.86,5.29,6.00,3.00,4,#2F4193
Transformative Change,Project Manager,TransformativeProject,5.00,2.25,2.75,3.00,5.00,5.25,3.00,4,#2F4193
Transformative Change,Scientist,TransformativeScientist,4.33,1.33,1.67,2.67,4.33,5.33,3.00,4,#2F4193
Transformative Change,Student,TransformativeStudent,4.40,3.40,4.00,4.20,4.40,5.40,3.00,4,#2F4193
""",
        content_type="text/plain",
    )

    return _dataframe_response(df, index=False)


def csv_heatmap(request, project):
    ownProject = Project.objects.get(pk=project)
    _authenticate_request(request, ownProject)

    return shortcuts.HttpResponse(
        """Principle,Dimension,Indicator,Value
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

