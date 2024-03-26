
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from selenium.webdriver.chrome.service import Service as ChromeService 
from subprocess import CREATE_NO_WINDOW

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmb

from PIL import Image 
import time
import winsound
import keyboard
import shutil
import os

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmb

import re

from Usuario import *


class Robot(webdriver.Chrome) :

	def __init__(self):
		
		chrome_service = ChromeService()
		chrome_service.creation_flags = CREATE_NO_WINDOW

		super().__init__(service=chrome_service)
		self.getAuth = None
		self.maximize_window()
		self.implicitly_wait(0.3)
		
		self.loggedInSEI = False
		self.loggedInSC = False
		
		self.root = None
		
		self.windowHandle = self.current_window_handle
	
	def logInSistemasCorporativos(self) :

		self.unminimize()
		self.get("http://sistemas2.utfpr.edu.br")
		
		if not self.loggedInSC:
			userbox = self.find_element(By.XPATH, "//input[@placeholder='Login']")
			passbox = self.find_element(By.XPATH, "//input[@placeholder='Senha']")
			button = self.find_element(By.XPATH, "//p-button")

			auth = self.getAuth()
			userbox.send_keys(auth.username)
			passbox.send_keys(auth.password)
			button.click()
			
			loop = True
			while loop:
				try:
					self.find_element(By.XPATH, "//span[contains(.,'Curitiba')]").click()
					loop = False
				except:
					pass
			
			self.loggedInSC = True
		
	def logInSEI(self):

		self.unminimize()
		self.get("http://sei.utfpr.edu.br")
	
		if not self.loggedInSEI:
		
			userbox = self.find_element(By.XPATH, "//input[@id='txtUsuario']")
			passbox = self.find_element(By.XPATH, "//input[@id='pwdSenha']")
			button = self.find_element(By.XPATH, "//button[@id='sbmAcessar']")
			
			auth = self.getAuth()			
			userbox.send_keys(auth.username)
			passbox.send_keys(auth.password)
			button.click()	
			
			self.loggedInSEI = True

	def iniciarProcessoSEI(self, tipo):
	
		self.find_element(By.XPATH, "//span[contains(.,'Iniciar Processo')]").click()
		self.find_element(By.LINK_TEXT, tipo).click()
	
		if tipo == "Patrimônio: Solicitação de Transferência de Bens" :
			self.find_element(By.ID, "btnSalvar").click()
	
	def incluirDocumento_ORIGINAL(self, tipo, info=""):
		self.find_element(By.XPATH, "//img[@alt='Incluir Documento']").click()
		self.find_element(By.LINK_TEXT, tipo).click()
		
		if tipo == "Patrimônio: Solicitação de Transferência de Bem":
			self.find_element(By.ID, "btnSalvar").click()
		elif tipo == "Cadastro Aluno UTFPR como usuário externo no SEI":
			self.find_element(By.ID, "txtNumero").send_keys(info)
			self.find_element(By.ID, "btnSalvar").click()
	
	def incluirDocumento(self, tipo, info=""):
		
		butt = None
		
		loop = True
		while loop:
			try:
				butt = self.find_element(By.XPATH, "//img[@alt='Incluir Documento']")
				loop = False
			except:
				print("I'm stuck!")
				continue
		
		butt.click()
		self.find_element(By.LINK_TEXT, tipo).click()
		
		if tipo == "Patrimônio: Solicitação de Transferência de Bem":
			self.find_element(By.ID, "btnSalvar").click()
		elif tipo == "Cadastro Aluno UTFPR como usuário externo no SEI":
			self.find_element(By.ID, "txtNumero").send_keys(info)
			self.find_element(By.ID, "btnSalvar").click()

	def liberarAssinaturaExterna(self, nome, senha):
	
		self.find_element(By.XPATH, "//img[@alt='Gerenciar Liberações para Assinatura Externa']").click()
		selectEmailElement = self.find_element(By.ID, "selEmailUnidade")
		selectEmail = Select(selectEmailElement)
		selectEmail.select_by_index(1)
		
		self.find_element(By.ID, "txtUsuario").send_keys(nome)
		time.sleep(2)
		
		AC = ActionChains(self)
		AC.send_keys(Keys.DOWN)
		AC.send_keys(Keys.ENTER)
		AC.perform()
		
		self.find_element(By.ID, "txtDias").send_keys("30")
		self.find_element(By.ID, "pwdSenha").send_keys(senha)
		self.find_element(By.ID, "btnLiberar").click()

	def beep(self, freq=500, duration=100):
		winsound.Beep(freq, duration)
		
	def waitKey(self, key="esc"):
		print("waiting for " + key + "...")
		keyboard.wait(key)

	def wait(self, time):
		time.sleep(time)

	def kill(self):
		self.quit()

	def changeUnidadeToF_DIRGRAD(self):
				
		unidades = self.find_elements(By.XPATH, "//a[@id='lnkInfraUnidade']")		
		
		if unidades[1].text != "F_DIRGRAD-CT":
			unidades[1].click()
		
			tds = self.find_elements(By.XPATH, "//td")
			for td in tds :
				if td.text == "F_DIRGRAD-CT":
					td.click()
					break

	def getStatusUsuarios(self, listaCods):
		
		usuarios = []
		
		for codUsuario in listaCods:
		
			novoUsuario = Usuario()
			if "." in codUsuario :
				novoUsuario.CPF.set(re.sub(r"[^0-9]", "", codUsuario))
				novoUsuario.externo = True
			else:
				novoUsuario.RA.set(re.sub(r"[^0-9]", "", codUsuario))
				
			usuarios.append(novoUsuario)
		
		self.logInSistemasCorporativos()
		
		atLeastOne = False
		
		for usuario in usuarios :
		
			if usuario.externo:
				next
		
			self.get("https://sistemas2.utfpr.edu.br/dpls/sistema/acad01/mpdeclaracoes.inicioconsulta")
			
			# preenche o RA do aluno na caixa de texto "Aluno"
			self.find_element(By.ID, "p_pessoa").send_keys(usuario.RA.get())
			AC = ActionChains(self)
			AC.send_keys(Keys.ENTER)
			AC.perform()
			
			# esse while abaixo lida com os elementos select da página de informações do aluno
			# o código ainda é propenso a erros, qualquer erro nessa tela vai levar o aluno
			# a ser considerado inexistente no sistema
			
			loopCounter = 0 # contador watchdog
			cursoIndex = 0
			while True :
				
				# contador watchdog, se exceder o número de loops, aluno é considerado inexistente
				loopCounter = loopCounter + 1
				if loopCounter > 10 :
					usuario.status = "INEXISTENTE"
					break
				
				cursoIndex = cursoIndex + 1
			
				# select "Curso/Aluno"
				# seleciona opção de index cursoIndex
				# caso não localize o select, aluno é considerado inexistente
				try:
					selectCursoElement = WebDriverWait(self, 1).until(
						EC.presence_of_element_located((By.XPATH, "//select[@id='p_curscodnr']"))
					)
					selectCurso = Select(selectCursoElement)
					selectCurso.select_by_index(cursoIndex)
				except:
					if self.find_element(By.XPATH, "//div[@id='divcombopessoa']").text == "Nenhum registro encontrado!" :
						usuario.status = "INEXISTENTE"
						break

				# select "Ano/Período"
				# esse select pode não existir!
				# se existe e encontrar a opção que diz "Regular", vá para o próximo select
				# se existe e não encontrar a opção que diz "Regular", vá para o próximo curso, no topo do while
				# se não existe e no lugar dele tem um div que não está escrito "Regular", vá para o próximo curso, no topo do while
				# se não existe e no lugar dele tem um div que está escrito "Regular", vá para o próximo select
				try:
				
					selectPeriodoElement = WebDriverWait(self, 1).until(
						EC.presence_of_element_located((By.XPATH, "//select[@id='p_alcuordemnr']"))
					)
					selectPeriodo = Select(selectPeriodoElement)

					found = False
					for option in selectPeriodo.options:
						if option.text.find("Regular") != -1 :
							selectPeriodo.select_by_visible_text(option.text)
							found = True
							break
							
					if not Found:
						continue
						
				except:
					if self.find_element(By.XPATH, "//div[@id='divcombopessoaordem']").text.find("Regular") == -1 :
						continue


				# select "Tipo de Declaração"
				# se existe, tente selecionar a primeira opção
				# se a primeira opção existe, clicar em "Procurar", segue a vida
				# se a primeira opção não existe, vá para o próximo curso, no topo do while
				# se não existe, vá para o próximo curso no topo do while
				
				try:
					selectDeclaracaoElement = WebDriverWait(self, 1).until(
						EC.presence_of_element_located((By.XPATH, "//select[@id='p_dofitiponr']"))
					)
					selectDeclaracao = Select(selectDeclaracaoElement)
				except:
					continue
				
				try:
					selectDeclaracao.select_by_index(1)
					break
				except:
					continue
		
			
			if usuario.status == "INEXISTENTE" :

				answer = tkmb.Message(self.root, message="Prosseguir?", type=tkmb.YESNO, icon=tkmb.QUESTION).show()
				
				if tkmb.YES :
					usuario.status = "DESCONHECIDO"
				else:
					usuario.status = "INEXISTENTE"
					
			
			# aluno existe e é possível gerar declaração para um curso "Regular"
			
			if usuario.status != "INEXISTENTE" :
			
				self.find_element(By.XPATH, "//button[@id='btnProcurar1']").click()

				# tente encontrar a foto do aluno
				# se existe, faça o screenshot
				# se não existe, marque aluno sem foto e segue a vida
				try:
					fotoElement = WebDriverWait(self, 2).until(
						EC.presence_of_element_located((By.XPATH, "//img[@alt='Foto']"))
					)
				
					time.sleep(1.5)
					fotoElement.screenshot(usuario.RA.get() + "face.png")
					usuario.hasPic = True
				except:
					pass

				# clique em "Gerar Declaração com Hash Validação"
				self.find_element(By.XPATH, "//button[@id='bt_geraDeclaracao']").click()
				
				
				
				# aguarde a nova janela abrir e mude o contexto para ela, salvando o contexto original
				original_window = self.current_window_handle
				while len(self.window_handles) < 2:
					time.sleep(0.1)
				self.switch_to.window(self.window_handles[1])
				
				# reposicione, redimensione e tire o screenshot da janela
				self.set_window_position(0, 0)
				self.set_window_size(943, 1000)
				table = self.find_element(By.XPATH, "//table")
				table.screenshot(usuario.RA.get() + ".png")
				
				# tome as informações listadas e atualize os atributos do aluno
				# atenção: é possível que este código interprete mal os dados
				# isso porque nem sempre os dados seguem o padrão presumido
				data = table.text.split("\n")
				
				for line in data :
					splitted = line.split(":")
				
					if splitted[0] == "Discente" :
						word = splitted[1].split("-")
						usuario.nome.set(word[1][1:None])
					elif splitted[0] == "CPF":
						usuario.CPF.set(splitted[1][1:None])
					elif splitted[0] == "RG":
						word = splitted[1].split(" ")
						for element in word:
							if element != "" :
								if element[0] == "[" :
									usuario.SSP.set(element[0][1:-1])
								else:
									usuario.RG.set(element)
						
						if usuario.SSP.get() == "":
							usuario.SSP.set("SSP")
					
					elif splitted[0] == "E-mail de Preferência":
						usuario.email.set(splitted[1][1:None])
					elif splitted[0] == "País":
						usuario.pais.set(splitted[1][1:None])
					elif splitted[0] == "UF":
						usuario.UF.set(splitted[1][1:None])
					elif splitted[0] == "Município":
						usuario.cidade.set(splitted[1][1:None])
					elif splitted[0] == "Logradouro/Número":
						usuario.endereco.set(splitted[1][1:None])
					elif splitted[0] == "Complemento":
						usuario.complemento.set(splitted[1][1:None])
					elif splitted[0] == "Bairro":
						usuario.bairro.set(splitted[1][1:None])
					elif splitted[0] == "CEP":
						usuario.CEP.set(splitted[1][1:None])
					elif splitted[0] == "Telefone":
						if usuario.telefoneCelular.get() == "":
							usuario.telefoneCelular.set(splitted[1][1:None])
						elif usuario.telefoneResidencial.get() == "" :
							usuario.telefoneResidencial.set(splitted[1][1:None])
						elif usuario.telefoneComercial.get() == "":
							usuario.telefoneComercial.set(splitted[1][1:None])

				usuario.status = "INFO COLETADA"
				atLeastOne = True

				# fecha a janela e retorna ao contexto original
				self.close()
				self.switch_to.window(original_window)
		
		# se tem pelo menos um aluno existente com dados, verifique se os alunos estão ativos ou não
		if atLeastOne :
			self.logInSEI()
			
			# a ordem das duas linhas abaixo importa, não mexa!
			self.getInativos(usuarios)
			self.getAtivos(usuarios)
		
		return usuarios

	def getInativos(self, alunos):
		
		self.changeUnidadeToF_DIRGRAD()
		self.find_element(By.XPATH, "//span[contains(.,'Cadastro de Usuário Externo')]").click()
		self.find_element(By.XPATH, "//a[@link='md_ce_ue_reativar']").click()
		
		for aluno in alunos:
			
			if aluno.status == "INFO COLETADA":
				
				cpfField = self.find_element(By.ID, "txtCpfUsuario")
				cpfField.clear()
				cpfField.send_keys(aluno.CPF.get())
				self.find_element(By.ID, "btnPesquisar").click()
				
				try:
					WebDriverWait(self, 0.5).until(
						EC.presence_of_element_located((By.XPATH, "//table[@summary='Tabela de Usuários Externos Inativos.']"))
					)
					
					# encontrou a tabela, agora isole o status
					infraTrClara = self.find_element(By.XPATH, "//tr[@class='infraTrClara']")
					td = self.find_elements(By.XPATH, "//td")
					aluno.status = td[3].text.upper()
				except:
					continue
	
	def getAtivos(self, alunos):
	
		self.changeUnidadeToF_DIRGRAD()
		self.find_element(By.XPATH, "//a[@link='md_ce_ue_listar']").click()

		for aluno in alunos:
		
			if aluno.status == "INFO COLETADA":
			
				cpfField = self.find_element(By.ID, "txtCpfUsuario")
				cpfField.clear()
				cpfField.send_keys(aluno.CPF.get())
				self.find_element(By.ID, "btnPesquisar").click()
				
				try:
					WebDriverWait(self, 0.5).until(
						EC.presence_of_element_located((By.XPATH, "//table[@summary='Tabela de Usuários Externos.']"))
					)
					
					# se a tabela existe, isole a informação do status
					infraTrClara = self.find_element(By.XPATH, "//tr[@class='infraTrClara']")
					td = self.find_elements(By.XPATH, "//td")
					aluno.status = td[3].text.upper()
				except:
					continue
				
	
		self.minimize()
	
	def inserirTermos(self, alunos, procSEI, password):
	
		for aluno in alunos :
		
			if aluno.cadastrar.get() == "1" : 
		
				self.switch_to.default_content()
			
				self.find_element(By.ID, "txtPesquisaRapida").send_keys(procSEI)
				self.find_element(By.XPATH, "//img[@alt='Pesquisa Rápida']").click()
				
				frame = self.find_element(By.ID, "ifrVisualizacao")
				self.switch_to.frame(frame)
				
				self.incluirDocumento("Cadastro Aluno UTFPR como usuário externo no SEI", aluno.nome.get())
				
				original_window = self.current_window_handle
					
				#wait for window to appear
				while len(self.window_handles) < 2:
					time.sleep(0.1)
				
				self.switch_to.window(self.window_handles[1])
			
				time.sleep(4)
			
				AC = ActionChains(self)
				AC.send_keys(Keys.TAB)
				AC.perform()
				
				AC.send_keys(Keys.TAB)
				AC.send_keys(Keys.TAB)
				AC.send_keys(Keys.DOWN)
				AC.send_keys(Keys.DOWN)
				AC.send_keys(Keys.TAB)
				AC.send_keys(Keys.TAB)
				
				AC.key_down(Keys.SHIFT)
				for i in range(0, 5):
					AC.send_keys(Keys.DOWN)
				AC.key_up(Keys.SHIFT)
				AC.perform()
				
				#inserir imagem
				self.find_element(By.XPATH, "//a[@id='cke_181']/span").click()
				time.sleep(1)
				
				AC.send_keys(Keys.SPACE)
				AC.perform()
				time.sleep(3)
				
				#os.path.abspath(aluno.RA.get() + ".png")
				keyboard.write(os.path.abspath(aluno.RA.get() + ".png"))
				keyboard.send("enter")
				time.sleep(1)
				
				keyboard.send("tab")
				time.sleep(1)
				keyboard.send("enter")
				time.sleep(1)
				
				#ctrl+alt+s - salvar
				AC.key_down(Keys.CONTROL)
				AC.key_down(Keys.ALT)
				AC.key_down("s")
				AC.key_up("s")
				AC.key_up(Keys.CONTROL)
				AC.key_up(Keys.ALT)
				AC.perform()
				
				time.sleep(2)
				
				self.close()
				self.switch_to.window(original_window)
				
				frame = self.find_element(By.ID, "ifrVisualizacao")
				self.switch_to.frame(frame)
				
				self.liberarAssinaturaExterna(aluno.nome.get(), password)

	def processarCadastros(self, alunos, procSEI, password):
	
		# possibilidades para aluno.status
		# DESCONHECIDO <- houve algum erro, não faça nada!
		# INEXISTENTE <- não faça nada!
		# INFO COLETADA <- faça o cadastro normalmente.
		# ATIVO <- não faça nada!
		# INATIVO <- ative
			# clicar em "Reativar Usuário Externo" e depois em "OK"
		# ATIVO E PENDENTE <- ative
			# clique em "Alterar Usuário Externo", depois no checkbutton "Liberado", depois no botão "Salvar"
		# INATIVO E PENDENTE
			# clicar em "Reativar Usuário Externo", depois em "OK", daí então
			# clique em "Alterar Usuário Externo", depois no checkbutton "Liberado", depois no botão "Salvar"
	
	
		self.logInSEI()
		self.changeUnidadeToF_DIRGRAD()
	
		for aluno in alunos :
	
			if aluno.cadastrar.get() == "1" : 
			
				# cadastar/ativar este aluno
				
				if aluno.status == "INFO COLETADA":
	
					# aluno não ativo ou pendente
					# vá até a tela de cadastro e preencha os campos
		
					self.find_element(By.XPATH, "//span[contains(.,'Cadastro de Usuário Externo')]").click()
					self.find_element(By.XPATH, "//span[contains(.,'Novo')]").click()
					
					self.find_element(By.ID, "txtNome").send_keys(aluno.nome.get())
					self.find_element(By.ID, "txtCpf").send_keys(aluno.CPF.get())
					self.find_element(By.ID, "txtRg").send_keys(aluno.RG.get())
					self.find_element(By.ID, "txtExpedidor").send_keys(aluno.SSP.get())
					self.find_element(By.ID, "txtTelefoneComercial").send_keys(aluno.telefoneComercial.get())
					self.find_element(By.ID, "txtTelefoneCelular").send_keys(aluno.telefoneCelular.get())
					self.find_element(By.ID, "txtTelefoneResidencial").send_keys(aluno.telefoneResidencial.get())
					self.find_element(By.ID, "txtEndereco").send_keys(aluno.endereco.get())
					self.find_element(By.ID, "txtComplemento").send_keys(aluno.complemento.get())
					self.find_element(By.ID, "txtBairro").send_keys(aluno.bairro.get())
				
					AC = ActionChains(self)
					AC.send_keys(Keys.TAB)
					AC.send_keys(aluno.pais.get())
					AC.send_keys(Keys.TAB)
					AC.send_keys(aluno.UF.get())
					AC.perform()
					
					time.sleep(0.3)
					
					AC.send_keys(Keys.TAB)
					AC.send_keys(aluno.cidade.get())
					AC.send_keys(Keys.TAB)
					AC.perform()
					
					self.find_element(By.ID, "txtCep").send_keys(aluno.CEP.get())
					self.find_element(By.ID, "txtEmail").send_keys(aluno.email.get())
					
					self.find_element(By.ID, "sbmEnviar").click()
					
					alert = WebDriverWait(self, 3).until(EC.alert_is_present())

					if alert.text == "Usuário Cadastrado com sucesso" :
						aluno.status = "CADASTRADO"
					else:
						aluno.status = "FALHA CADASTRO"
					
					time.sleep(1.5)
					alert.accept()
					
				elif aluno.status == "INATIVO":
					
					# vá até a tela de inativos, preencha o CPF e pesquise
					self.find_element(By.XPATH, "//span[contains(.,'Cadastro de Usuário Externo')]").click()
					self.find_element(By.XPATH, "//a[@link='md_ce_ue_reativar']").click()
					
					cpfField = self.find_element(By.ID, "txtCpfUsuario")
					cpfField.clear()
					cpfField.send_keys(aluno.CPF.get())
					self.find_element(By.ID, "btnPesquisar").click()
					
					try:
						WebDriverWait(self, 0.5).until(
							EC.presence_of_element_located((By.XPATH, "//table[@summary='Tabela de Usuários Externos Inativos.']"))
						)
						
						# encontrou a tabela, clique em "Reativar Usuário Externo"
						self.find_element(By.XPATH, "//img[@title='Reativar Usuário Externo']").click()
						
						alert = WebDriverWait(self, 3).until(EC.alert_is_present())

						if alert.text.find("Confirma reativação") != -1:
							aluno.status = "ATIVADO"
						else:
							aluno.status = "FALHA ATIVAÇÃO"
	
						alert.accept()
						time.sleep(1.5)
						
					except:
						aluno.status = "FALHA ATIVAÇÃO"
						continue
					
				elif aluno.status == "ATIVO E PENDENTE":
					
					# vá até a tela de ativos, preencha o CPF e pesquisa
					self.find_element(By.XPATH, "//span[contains(.,'Cadastro de Usuário Externo')]").click()
					self.find_element(By.XPATH, "//a[@link='md_ce_ue_reativar']").click()
					
					cpfField = self.find_element(By.ID, "txtCpfUsuario")
					cpfField.clear()
					cpfField.send_keys(aluno.CPF.get())
					self.find_element(By.ID, "btnPesquisar").click()
					
					try:
						WebDriverWait(self, 0.5).until(
							EC.presence_of_element_located((By.XPATH, "//table[@summary='Tabela de Usuários Externos Inativos.']"))
						)
						
						# encontrou a tabela, clique em "Alterar Usuário Externo"
						self.find_element(By.XPATH, "//img[@title='Alterar Usuário Externo']").click()
						
						#escolher "Liberar" e "Salvar"
						#self.find_element(By.XPATH, "//input[@id='optLiberado']").click()
						self.find_element(By.XPATH, "//div[@id='divOptLiberado']/div/label").click()
						self.find_element(By.XPATH, "//button[@name='sbmAlterarUsuario']").click()
						
					except:
						print("falha de ativação")
						aluno.status = "FALHA ATIVAÇÃO (PENDENTE)"
						continue
					
				
		self.inserirTermos(alunos, procSEI, password)
	
		self.minimize()
	
	def unminimize(self):
		self.switch_to.window(self.windowHandle)
		self.maximize_window()
		
	def minimize(self):
		self.minimize_window()
		
