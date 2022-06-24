Sub AddData()

    Dim wb As Workbook
    Dim ws As Worksheet
    Dim FoundCell As Range
    Set wb = ActiveWorkbook
    Set ws = ActiveSheet
    
    Dim WHAT_TO_FIND As Integer
    WHAT_TO_FIND = ws.Range("B10")
    
    Dim ROW As String
    ROW = CStr(ws.Range("B11"))
    MsgBox (ROW)
    'ThisWorkbook.Worksheets("Pesquisa de Mercado").Range ("B11").
    
    Dim nome As String
    Dim endereco As String
    Dim numero As Integer
    Dim complemento As String
    Dim bairro As String
    Dim cep As String
    Dim municipio As String
    Dim uf As String
    Dim tipo As String
    Dim lead As String
    

    Set FoundCell = ws.Range("F:F").Find(What:=WHAT_TO_FIND)
    If Not FoundCell Is Nothing Then
        'MsgBox (WHAT_TO_FIND & " found in row: " & FoundCell.Row).
        nome = ws.Range("G" + CStr(FoundCell.ROW))
        endereco = ws.Range("H" + CStr(FoundCell.ROW))
        numero = ws.Range("I" + CStr(FoundCell.ROW))
        complemento = ws.Range("J" + CStr(FoundCell.ROW))
        bairro = ws.Range("K" + CStr(FoundCell.ROW))
        cep = ws.Range("L" + CStr(FoundCell.ROW))
        municipio = ws.Range("M" + CStr(FoundCell.ROW))
        uf = ws.Range("N" + CStr(FoundCell.ROW))
        tipo = ws.Range("O" + CStr(FoundCell.ROW))
        lead = ws.Range("P" + CStr(FoundCell.ROW))
        
        ThisWorkbook.Worksheets("Avaliação de Imóveis").Range("I" + ROW).Value = lead
        ThisWorkbook.Worksheets("Avaliação de Imóveis").Range("J" + ROW).Value = nome
        ThisWorkbook.Worksheets("Avaliação de Imóveis").Range("L" + ROW).Value = municipio
        ThisWorkbook.Worksheets("Avaliação de Imóveis").Range("M" + ROW).Value = uf
        ThisWorkbook.Worksheets("Avaliação de Imóveis").Range("N" + ROW).Value = endereco
        ThisWorkbook.Worksheets("Avaliação de Imóveis").Range("O" + ROW).Value = numero
        ThisWorkbook.Worksheets("Avaliação de Imóveis").Range("P" + ROW).Value = complemento
        ThisWorkbook.Worksheets("Avaliação de Imóveis").Range("Q" + ROW).Value = bairro
        ThisWorkbook.Worksheets("Avaliação de Imóveis").Range("R" + ROW).Value = cep
        
        
        
        With ws.Range("B11")
            .Value = .Value + 1
        End With

        
    Else
        MsgBox (WHAT_TO_FIND & " not found")
    End If
    
End Sub

Sub SearchLaudos()
    Call Shell("cmd.exe /S /K" & """python C:\Users\tdoliveira\Documents\automatizacao-laudos-python\get_email_data\main.py""", vbNormalFocus)
End Sub


Sub UpdateLaudos()
    Dim DataFile As String
    Dim OpenBook As Workbook
    
    
    DataFile = Application.ActiveWorkbook.Path + "\novos_laudos.xlsx"
    
    ThisWorkbook.Worksheets("Email").Range("F1").CurrentRegion.Clear
    
    Set OpenBook = Application.Workbooks.Open(DataFile)
    OpenBook.Sheets(1).Range("A1").CurrentRegion.Copy
    
    ThisWorkbook.Worksheets("Email").Range("F1").PasteSpecial xlPasteValues
    OpenBook.Close False
    
    Application.ScreenUpdating = True
End Sub
