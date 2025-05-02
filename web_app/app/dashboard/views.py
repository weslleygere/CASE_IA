from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import ModelTestForm
import pickle
import os
from django.conf import settings
from .ia_model.pre_processing import preprocess_input

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

class ConfigView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/config.html'

class ModelTestView(LoginRequiredMixin, FormView):
    template_name = 'dashboard/test_model.html'
    form_class = ModelTestForm
    success_url = reverse_lazy('test_model')

    def form_valid(self, form):
        # 1️⃣ Coletar os dados informados no formulário
        data_dict = {
            'X1': form.cleaned_data['Relative_Compactness'],
            'X2': form.cleaned_data['Surface_Area'],
            'X3': form.cleaned_data['Wall_Area'],
            'X4': form.cleaned_data['Roof_Area'],
            'X5': form.cleaned_data['Overall_Height'],
            'X6': form.cleaned_data['Orientation'],
            'X7': form.cleaned_data['Glazing_Area'],
            'X8': form.cleaned_data['Glazing_Area_Distribution'],
        }

        # 2️⃣ Pré-processar os dados
        X_input = preprocess_input(data_dict, nome_conjunto='baseline')

        # 3️⃣ Carregar o modelo treinado
        model_path = os.path.join(settings.BASE_DIR, 'dashboard', 'ia_model', 'model.pkl')
        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        # 4️⃣ Fazer a predição
        y_pred = model.predict(X_input)

        # 5️⃣ Interpretar as saídas
        if hasattr(y_pred[0], '__iter__') and len(y_pred[0]) == 2:
            carga_aquecimento = round(y_pred[0][0], 2)
            carga_resfriamento = round(y_pred[0][1], 2)
        else:
            carga_aquecimento = round(y_pred[0], 2)
            carga_resfriamento = None

        # 6️⃣ Retornar os resultados no template
        return self.render_to_response(self.get_context_data(
            form=form,
            carga_aquecimento=carga_aquecimento,
            carga_resfriamento=carga_resfriamento
        ))


