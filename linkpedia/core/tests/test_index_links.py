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
    
    def test_requires_login(self):

        # Criando uma rota temporária
        response = self.client.get(
            reverse('table')
        )

        # Redirecionando o usuário que não possui login
        self.assertEqual(response.status_code, 302)

    def test_template(self):
        # Criando um usuário temporário
        user = User.objects.create_user(
            username='aluno',
            password='fatec'
        )

        # Logando o usuário temporáriamente
        self.client.login(
            username='aluno',
            password='fatec'
        )

        # Criando o redirecionamento temporário
        response = self.client.get(
            reverse('table')
        )

        # Testando qual template é rediorecionado
        self.assertTemplateUsed(
            response, 'table.html'
        )