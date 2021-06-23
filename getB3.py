import urllib.request, zipfile, argparse, datetime, os, glob, io


# Extract B3 history

def extract_b3_history(min,max): 

	internal_range = range(min,max)
	download_url='http://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A'
	file_extension='.zip'
	save_path='./'
	urls=[download_url+str(i)+file_extension for i in internal_range]
	names=[save_path+str(i)+file_extension for i in internal_range]

	for j in range(len(urls)):
	    url = urls[j]
	    name = names[j]
	    urllib.request.urlretrieve(url, name)
	    with zipfile.ZipFile(name, 'r') as file_zipped:
	    	file_zipped.extractall(save_path)


# Parse B3 history File (if it is TXT)

def read_b3_history(filename, cod):

	#print('Reading history file '+filename)

	read_file = io.open(filename, 'r', encoding="ISO-8859-1") 
	lines = read_file.readlines() 


	bdi_codes_dict = { 
		"02": "LOTE PADRAO",
		"05" :"SANCIONADAS PELOS REGULAMENTOS BMFBOVESPA",
		"06" :"CONCORDATARIAS",
		"07" :"RECUPERACAO EXTRAJUDICIAL",
		"08" :"RECUPERAÇÃO JUDICIAL",
		"09" :"RAET - REGIME DE ADMINISTRACAO ESPECIAL TEMPORARIA",
		"10" :"DIREITOS E RECIBOS",
		"11" :"INTERVENCAO",
		"12" :"FUNDOS IMOBILIARIOS",
		"14" :"CERT.INVEST/TIT.DIV.PUBLICA",
		"18" :"OBRIGACÕES",
		"22" :"BÔNUS (PRIVADOS)",
		"26" :"APOLICES/BÔNUS/TITULOS PUBLICOS",
		"32" :"EXERCICIO DE OPCOES DE COMPRA DE INDICES",
		"33" :"EXERCICIO DE OPCOES DE VENDA DE INDICES",
		"38" :"EXERCICIO DE OPCOES DE COMPRA",
		"42" :"EXERCICIO DE OPCOES DE VENDA",
		"46" :"LEILAO DE NAO COTADOS",
		"48" :"LEILAO DE PRIVATIZACAO",
		"49" :"LEILAO DO FUNDO RECUPERACAO ECONOMICA ESPIRITO SANTO",
		"50" :"LEILAO",
		"51" :"LEILAO FINOR",
		"52" :"LEILAO FINAM",
		"53" :"LEILAO FISET",
		"54" :"LEILAO DE ACÕES EM MORA",
		"56" :"VENDAS POR ALVARA JUDICIAL",
		"58" :"OUTROS",
		"60" :"PERMUTA POR ACÕES",
		"61" :"META",
		"62" :"MERCADO A TERMO",
		"66" :"DEBENTURES COM DATA DE VENCIMENTO ATE 3 ANOS",
		"68" :"DEBENTURES COM DATA DE VENCIMENTO MAIOR QUE 3 ANOS",
		"70" :"FUTURO COM RETENCAO DE GANHOS",
		"71" :"MERCADO DE FUTURO",
		"74" :"OPCOES DE COMPRA DE INDICES",
		"75" :"OPCOES DE VENDA DE INDICES",
		"78" :"OPCOES DE COMPRA",
		"82" :"OPCOES DE VENDA",
		"83" :"BOVESPAFIX",
		"84" :"SOMA FIX",
		"90" :"TERMO VISTA REGISTRADO",
	    "96" :"MERCADO FRACIONARIO",
		"99" :"TOTAL GERAL" 
		
	}

	mercado_dict = {
		"010": "VISTA",
		"012": "EXERCÍCIO DE OPÇÕES DE COMPRA",
		"013": "EXERCÍCIO DE OPÇÕES DE VENDA",
		"017": "LEILÃO",
		"020": "FRACIONÁRIO",
		"030": "TERMO",
		"050": "FUTURO COM RETENÇÃO DE GANHO",
		"060": "FUTURO COM MOVIMENTAÇÃO CONTÍNUA",
		"070": "OPÇÕES DE COMPRA",
		"080": "OPÇÕES DE VENDA"
	}


	espec_papel_dict = {
		"BDR" : "BDR",
		"BNS" :"BÔNUS DE SUBSCRIÇÃO EM ACÕES MISCELÂNEA",
		"BNS" :"B/A BÔNUS DE SUBSCRIÇÃO EM ACÕES PREFERÊNCIA",
		"BNS" :"ORD BÔNUS DE SUBSCRIÇÃO EM ACÕES ORDINÁRIAS",
		"BNS" :"P/A BÔNUS DE SUBSCRIÇÃO EM ACÕES PREFERÊNCIA",
		"BNS" :"P/B BÔNUS DE SUBSCRIÇÃO EM ACÕES PREFERÊNCIA",
		"BNS" :"P/C BÔNUS DE SUBSCRIÇÃO EM ACÕES PREFERÊNCIA",
		"BNS" :"P/D BÔNUS DE SUBSCRIÇÃO EM ACÕES PREFERÊNCIA",
		"BNS" :"P/E BÔNUS DE SUBSCRIÇÃO EM ACÕES PREFERÊNCIA",
		"BNS" :"P/F BÔNUS DE SUBSCRIÇÃO EM ACÕES PREFERÊNCIA",
		"BNS" :"P/G BÔNUS DE SUBSCRIÇÃO EM ACÕES PREFERÊNCIA",
		"BNS" :"P/H BÔNUS DE SUBSCRIÇÃO EM ACÕES PREFERÊNCIA",
		"BNS" :"PRE BÔNUS DE SUBSCRIÇÃO EM ACÕES PREFERÊNCIA",
		"CDA" :"CERTIFICADO DE DEPÓSITO DE ACÕES ORDINÁRIAS",
		"CI"  :"FUNDO DE INVESTIMENTO",
		"CI"  :"ATZ Fundo de Investimento Atualização",
		"CI"  :"EA Fundo de Investimento Ex-Atualização",
		"CI"  :"EBA Fundo de Investimento Ex-Bonificação e Ex-Atualização",
		"CI"  :"ED Fundo de Investimento Ex-dividendo",
		"CI"  :"ER Fundo de Investimento Ex-Rendimento",
		"CI"  :"ERA Fundo de Investimento Ex-rendimento e Ex-Atualização",
		"CI"  :"ERB Fundo de Investimento Ex-rendimento e Ex-Bonificação",
		"CI"  :"ERS Fundo de Investimento Ex-Rendimento e Ex-Subscrição",
		"CI"  :"ES Fundo de Investimento Ex-Subscrição",
		"CPA" :"CERTIF. DE POTENCIAL ADIC. DE CONSTRUÇÃO",
		"DIR" :"DIREITOS DE SUBSCRIÇÃO MISCELÂNEA (BÔNUS)",
		"DIR" :"DEB Direito de Debênture",
		"DIR" :"ORD DIREITOS DE SUBSCRIÇÃO EM ACÕES ORDINÁRIAS",
		"DIR" :"P/A DIREITOS DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS",
		"DIR" :"P/B DIREITOS DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS",
		"DIR" :"P/C DIREITOS DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS",
		"DIR" :"P/D DIREITOS DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS",
		"DIR" :"P/E DIREITOS DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS",
		"DIR" :"P/F DIREITOS DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS",
		"DIR" :"P/G DIREITOS DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS",
		"DIR" :"P/H DIREITOS DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS",
		"DIR" :"PR DIREITOS DE SUBSCRIÇÃO EM ACÕES RESGATÁVEIS",
		"DIR" :"PRA DIREITOS DE SUBSCRIÇÃO EM ACÕES RESGATÁVEIS",
		"DIR" :"PRB DIREITOS DE SUBSCRIÇÃO EM ACÕES RESGATÁVEIS",
		"DIR" :"PRC DIREITOS DE SUBSCRIÇÃO EM ACÕES RESGATÁVEIS",
		"DIR" :"PRE DIREITOS DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS",
		"FIDC" :"Fundo de Investimento em Direitos Creditórios",
		"LFT" : "LETRA FINANCEIRA DO TESOURO",
		"M1" : "REC RECIBO DE SUBSCRIÇÃO DE MISCELÂNEAS",
		"ON" : "ACÕES ORDINÁRIAS NOMINATIVAS",
		"ON" : "ATZ Ações Ordinárias Atualização",
		"ON" : "EB Ações Ordinárias Ex-Bonificação",
		"ON" : "ED Ações Ordinárias Ex-Dividendo",
		"ON" : "EDB Ações Ordinárias Ex-Dividendo e Ex-Bonificação",
		"ON" : "EDJ Ações Ordinárias Ex-dividendo e Ex-Juros",
		"ON" : "EDR Ações Ordinárias Ex-Dividendo e Ex-Rendimento",
		"ON" : "EG Ações Ordinárias Ex-Grupamento",
		"ON" : "EJ Ações Ordinárias Ex-juros",
		"ON" : "EJB Ações Ordinárias Ex-juros e Ex-bonificação",
		"ON" : "EJS Ações Ordinárias Ex-Juros e Ex-Subscrição",
		"ON" : "ER Ações Ordinárias Ex-Rendimento",
		"ON" : "ERJ Ações Ordinárias Ex-Rendimento e Ex-Juros",
		"ON" : "ES Ações Ordinárias Ex-Subscrição",
		"ON" : "P ACÕES ORDINÁRIAS NOMINATIVAS COM DIREITO",
		"ON" : "REC RECIBO DE SUBSCRIÇÃO EM ACÕES ORDINÁRIAS",
		"OR" : "ACÕES ORDINÁRIAS NOMINATIVAS RESGATÁVEIS",
		"OR" : "P ACÕES ORDINÁRIAS NOMINATIVAS RESGATÁVEIS",
		"PCD" : "POSIÇÃO CONSOLIDADA DA DIVIDA",
		"PN" : "ACÕES PREFERÊNCIAIS NOMINATIVAS",
		"PN" : "EB Ações Preferenciais Ex-Bonificação",
		"PN" : "ED Ações Preferenciais Ex-Dividendo",
		"PN" : "EDB Ações Preferenciais Ex-Dividendo e Ex-Bonificação",
		"PN" : "EDJ Ações Preferenciais Ex-dividendo e Ex-Juros",
		"PN" : "EDR Ações Preferenciais Ex-Dividendo e Ex-Rendimento",
		"PN" : "EJ Ações Preferenciais Ex-Juros",
		"PN" : "EJB Ações Preferenciais Ex-juros e Ex-bonificação",
		"PN" : "EJS Ações Preferenciais Ex-Juros e Ex-Subscrição",
		"PN" : "ES Ações Preferenciais Ex-Subscrição",
		"PN" : "P ACÕES PREFERÊNCIAIS NOMINATIVAS COM DIREITO",
		"PN" : "REC RECIBO DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS",
		"PNA" : "ACÕES PREFERÊNCIAIS NOMINATIVAS CLASSE A",
		"PNA" : "EB Ações Preferenciais Classe A Ex-BonificaçãoPreferencial",
		"PNA" : "EDR Ações Preferenciais Classe A Ex-Dividendo e Ex-Rendimento",
		"PNA" : "EJ Ações Preferenciais Classe A Ex-Juros",
		"PNA" : "ES Ações Preferenciais Classe A Preferencial Ex-Subscrição",
		"PNA" : "P ACÕES PREFERÊNCIAIS NOMINATIVAS CLASSE A",
		"PNA" : "REC RECIBO DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS",
		"PNB" : "ACÕES PREFERÊNCIAIS NOMINATIVAS CLASSE B",
		"PNB" : "EB Ações Preferenciais Classe B Ex-Bonificação",
		"PNB" : "ED Ações Preferenciais Classe B Ex-Dividendo",
		"PNB" : "EDR Ações Preferenciais Classe B Ex-Dividendo e Ex-Rendimento",
		"PNB" : "EJ Ações Preferenciais Classe B Ex-Juros",
		"PNB" : "P ACÕES PREFERÊNCIAIS NOMINATIVAS CLASSE B",
		"PNB" : "REC RECIBO DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS",
		"PNC" : "ACÕES PREFERÊNCIAIS NOMINATIVAS CLASSE C",
		"PNC" : "ED Ações Preferenciais Classe C Preferencial Classe C Ex-Dividendo",
		"PNC" : "P ACÕES PREFERÊNCIAIS NOMINATIVAS CLASSE C",
		"PNC" : "REC RECIBO DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS",
		"PND" : "ACÕES PREFERÊNCIAIS NOMINATIVAS CLASSE D",
		"PND" : "ED Ações Preferenciais Classe D Ex-Dividendo",
		"PND" : "P ACÕES PREFERÊNCIAIS NOMINATIVAS CLASSE D",
		"PND" : "REC RECIBO DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS",
		"PNE" : "ACÕES PREFERÊNCIAIS NOMINATIVAS CLASSE E",
		"PNE" : "ED Ações Preferenciais Classe E Ex-Dividendo",
		"PNE" : "P ACÕES PREFERÊNCIAIS NOMINATIVAS CLASSE E",
		"PNE" : "REC RECIBO DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS"

	}
  
	count = 0
	
	#parse lines
	for line in lines: 

		tipo = line[0:2]          		# tipo registro 
		data = line[2:10]         		# data AAAAMMDD
		bdi = line[10:12]				# código BDI
		cod_papel = line[12:24]			# código papel
		mercado = line[24:27]			# tipo de mercado
		empresa = line[27:39]			# nome resumido empresa
		espec_papel = line[39:49]		# especificação do papel 
		prazo_term = line[49:52]		# prazo em dias de mercado a termo
		moeda = line[52:56]				# moeda referência
		preco_abertura = line[69:82] 	# preço de abertura do papel no mercado pregão
		preco_max = line[95:108]			# preço máximo do papel no mercado pregão
		preco_min = line[82:95] 		# preço mínimo do papel no mercado pregão
		preco_medio =line[108:121] 		# preço médio do papel no mercado pregão
		preco_fechamento = line[121:134]# último preço do papel no mercado pregão
		preco_melhor_compra =line[134:147] # preço da melhor oferta de compra do papel no mercado
		preco_melhor_venda = line[147:152] # preço da melhor oferta de venda do papel no mercado
		numero_negocios = line[152:170]			# número total de negócios do mercado pregão
		total_negocios = line[170:188]			# quantidade total de titulos negociados no mercado
		volume = line[188:201]					# volume total de negócios deste papel no mercado
		preco_exercicio = line[201:202]	
		indicador_correcao = line[202:202]		# preco exercicio 
		data_vencimento	= line[202:217]
		fator_cotacao = line[210:217]
		preco_exercicio_pontos = line[217:230]
		isin = line[230:242]
		numero_distribuicao = line[242:245]

		
		if (mercado == "010" and data > "20200101" and cod in cod_papel ):
			print(data+','+cod_papel.strip()+','+convert_strtomoney(preco_abertura)+','+convert_strtomoney(preco_fechamento)+','+convert_strtomoney(preco_min)+','+convert_strtomoney(preco_max)+','+convert_strtomoney(preco_medio)+','+numero_negocios)	

		read_file.close() 
		
def convert_strtomoney(number):
	return "{:0,.3f}".format(float(number[:-2]+'.'+number[-2:]))		

def main():
	
	extract_b3_history(1986,2021)

	for filename in glob.glob('*.TXT'):
		read_b3_history('./'+filename, 'MGLU3')

	
	

if __name__== "__main__":
   main()


