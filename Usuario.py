
import tkinter as tk

class Usuario :
	def __init__(self):
		self.nome = tk.StringVar(value="INVALIDO")
		self.nomeSocial = tk.StringVar(value="")
		self.RA = tk.StringVar(value="-X-")
		self.RG = tk.StringVar(value="")
		self.CPF = tk.StringVar(value="")
		self.SSP = tk.StringVar(value="")
		self.pais = tk.StringVar(value="")
		self.UF = tk.StringVar(value="")
		self.cidade = tk.StringVar(value="")
		self.telefoneComercial = tk.StringVar(value="")
		self.telefoneCelular = tk.StringVar(value="")
		self.telefoneResidencial = tk.StringVar(value="")
		self.endereco = tk.StringVar(value="")
		self.complemento = tk.StringVar(value="")
		self.bairro = tk.StringVar(value="")
		self.estado = tk.StringVar(value="")
		self.CEP = tk.StringVar(value="")
		self.email = tk.StringVar(value="")
		self.curso = tk.StringVar(value="-X-")
		self.estrangeiro = tk.StringVar(value="0")
		self.status = "DESCONHECIDO"
		self.hasPic = False
		self.facePic = None
		self.cadastrar = tk.StringVar(value="0")
		self.gerarTermo = tk.StringVar(value="0")
		self.externo = False

	def print(self):
		print(":::" + self.nome.get() + ":::")
		print("RA:" + self.RA.get())
		print("CPF:" + self.CPF.get())
		print("RG:" + self.RG.get())
		print("SSP:" + self.SSP.get())
		print("email:" + self.email.get())
		print("pais:" + self.pais.get())
		print("UF:" + self.UF.get())
		print("cidade:" + self.cidade.get())
		print("endereco:" + self.endereco.get())
		print("complemento:" + self.complemento.get())
		print("bairro:" + self.bairro.get())
		print("CEP:" + self.CEP.get())
		print("telefone celular:" + self.telefoneCelular.get())
		print("telefone residencial:" + self.telefoneResidencial.get())
		print("telefone comercial:" + self.telefoneComercial.get())
		print("STATUS:" + self.status)
		print("")
		print("")

	def __str__(self):
		str = ""
		str = str + ":::" + self.nome.get() + ":::" + "\n"
		str = str + "RA:" + self.RA.get() + "\n"
		str = str + "CPF:" + self.CPF.get() + "\n"
		str = str + "RG:" + self.RG.get() + "\n"
		str = str + "SSP:" + self.SSP.get() + "\n"
		str = str + "email:" + self.email.get() + "\n"
		str = str + "pais:" + self.pais.get() + "\n"
		str = str + "UF:" + self.UF.get() + "\n"
		str = str + "cidade:" + self.cidade.get() + "\n"
		str = str + "endereco:" + self.endereco.get() + "\n"
		str = str + "complemento:" + self.complemento.get() + "\n"
		str = str + "bairro:" + self.bairro.get() + "\n"
		str = str + "CEP:" + self.CEP.get() + "\n"
		str = str + "telefone celular:" + self.telefoneCelular.get() + "\n"
		str = str + "telefone residencial:" + self.telefoneResidencial.get() + "\n"
		str = str + "telefone comercial:" + self.telefoneComercial.get() + "\n"
		str = str + "STATUS:" + self.status + "\n"
		str = str + "\n"
		str = str + "\n"
		return str
		