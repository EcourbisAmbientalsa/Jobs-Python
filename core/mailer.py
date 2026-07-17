import os
import win32com.client as win32


class OutlookMailer:
    """Envia e-mail pelo Outlook desktop instalado na máquina"""

    def __init__(self, remetente=None):
        self.remetente = remetente

    def enviar(self, para, assunto, corpo, anexos=None, cc=None, html=True):
        outlook = win32.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)  # 0 = olMailItem

        mail.To = para if isinstance(para, str) else "; ".join(para)
        if cc:
            mail.CC = cc if isinstance(cc, str) else "; ".join(cc)

        mail.Subject = assunto

        if html:
            mail.HTMLBody = corpo
        else:
            mail.Body = corpo

        if self.remetente:
            mail.SentOnBehalfOfName = self.remetente

        for caminho in (anexos or []):
            if caminho and os.path.exists(caminho):
                mail.Attachments.Add(caminho)
            else:
                print(f"AVISO: anexo não encontrado: {caminho}")

        mail.Send()
        print(f"✔ E-mail enviado para: {mail.To}")