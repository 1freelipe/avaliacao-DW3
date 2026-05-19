from django.test import TestCase
from core.models import LinkModel
from django.contrib.auth.models import User
from django.urls import reverse

class LinkTest(TestCase):

    def test_table_requires_login(self):
        # testando se a rota está fechada apenas para usuários autenticados
        response = self.client.get(
            reverse('table')
        )
        # retornando o código 302 (redirect) se a rota estiver fechada
        self.assertEqual(response.status_code, 302)

    def test_table_authenticated(self):
        # Criar autenticação temporária
        user = User.objects.create_user(
            username='aluno',
            password='fatec'
        )

         # Logar com a autenticação temporária
        self.client.login(
            username='aluno',
            password='fatec'
        )

        response = self.client.get(
            reverse('table')
        )
        # retornando o status code 200 se o usuário conseguir acessar autenticado
        self.assertEqual(response.status_code, 200)
        