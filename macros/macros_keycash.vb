Sub RunPython()
    Set fs = CreateObject("Scripting.FileSystemObject")
    'Set a = fs.CreateTextFile("R:\Empirica Cobrancas e Garantias\5 - Avaliacoes de Imoveis\automatizacao-laudos-python\get_data\file.txt", True).
    Set a = fs.CreateTextFile("C:\Users\noliveira\Documents\automatizacao-laudos-python\get_data\file.txt", True)
    a.WriteLine (ThisWorkbook.FullName)

    'Endereco
    a.WriteLine (ThisWorkbook.Worksheets("Modelo de Laudo").Range("E22"))
    'numero
    a.WriteLine (ThisWorkbook.Worksheets("Modelo de Laudo").Range("Q22"))
    'bairro
    a.WriteLine (ThisWorkbook.Worksheets("Modelo de Laudo").Range("E23"))
    'municipio
    a.WriteLine (ThisWorkbook.Worksheets("Modelo de Laudo").Range("E24"))
    'uf
    a.WriteLine (ThisWorkbook.Worksheets("Modelo de Laudo").Range("U24"))
    'CEP
    a.WriteLine (ThisWorkbook.Worksheets("Modelo de Laudo").Range("U23"))
    'tipo
    a.WriteLine (ThisWorkbook.Worksheets("Modelo de Laudo").Range("E27"))

    'area
    a.WriteLine (ThisWorkbook.Worksheets("Modelo de Laudo").Range("U34"))
    a.Close
    
    Call Shell("cmd.exe /S /K" & """python C:\Users\noliveira\Documents\automatizacao-laudos-python\get_data\main.py""", vbNormalFocus)

End Sub

Sub UpdateData()
    Dim OpenBook As Workbook
    Dim DataFile As String
    Dim folder As String
    Dim DataFile2 As String
    Dim a As Variant
    
    DataFile = ActiveWorkbook.Path
    
    a = Split(DataFile, "/")
    folder = "C:/Users/noliveira/Empírica Investimentos Gestão de Recursos Ltda/ESCO - Documentos/5 - Avaliacoes de Imoveis/Keycash/" + a(8) + "/" + a(9)
    DataFile2 = folder + "/dados_coletados.xlsx"
    
    If a(0) = "https:" Then
        Set OpenBook = Application.Workbooks.Open(DataFile2)
    Else
        Set OpenBook = Application.Workbooks.Open(DataFile + "/dados_coletados.xlsx")
    End If
    
    OpenBook.Sheets(1).Range("A1").CurrentRegion.Copy
    ThisWorkbook.Worksheets("Dados Coletados").Range("F1").PasteSpecial xlPasteValues
    OpenBook.Close False
    
    Application.ScreenUpdating = True
    
End Sub

Sub DownloadImage1()
    Set fs = CreateObject("Scripting.FileSystemObject")
    Set a = fs.CreateTextFile("C:\Users\noliveira\Documents\automatizacao-laudos-python\get_images\file.txt", True)
    a.WriteLine (ThisWorkbook.FullName)
    a.WriteLine ("1" & vbNewLine & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("AO5") & vbNewLine & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q7") & vbNewLine & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q8"))
    a.Close

    Call Shell("cmd.exe /S /C" & """python C:\Users\noliveira\Documents\automatizacao-laudos-python\get_images\main.py""", vbNormalFocus)
    
    
     With ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("AO5")
        .Value = .Value + 1
    End With
    
End Sub

Sub DownloadImage2()
    Set fs = CreateObject("Scripting.FileSystemObject")
    Set a = fs.CreateTextFile("C:\Users\noliveira\Documents\automatizacao-laudos-python\get_images\file.txt", True)
    a.WriteLine (ThisWorkbook.FullName)
    a.WriteLine ("2" & vbNewLine & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("AO17") & vbNewLine & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q19") & vbNewLine & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q20"))
    a.Close

    Call Shell("cmd.exe /S /C" & """python C:\Users\noliveira\Documents\automatizacao-laudos-python\get_images\main.py""", vbNormalFocus)
    
    
     With ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("AO17")
        .Value = .Value + 1
    End With
    
End Sub

Sub DownloadImage3()
    Set fs = CreateObject("Scripting.FileSystemObject")
    Set a = fs.CreateTextFile("C:\Users\noliveira\Documents\automatizacao-laudos-python\get_images\file.txt", True)
    a.WriteLine (ThisWorkbook.FullName)
    a.WriteLine ("3" & vbNewLine & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("AO29") & vbNewLine & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q31") & vbNewLine & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q32"))
    a.Close

    Call Shell("cmd.exe /S /C" & """python C:\Users\noliveira\Documents\automatizacao-laudos-python\get_images\main.py""", vbNormalFocus)
    
    
     With ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("AO29")
        .Value = .Value + 1
    End With
    
End Sub

Sub DownloadImage4()
    Set fs = CreateObject("Scripting.FileSystemObject")
    Set a = fs.CreateTextFile("C:\Users\noliveira\Documents\automatizacao-laudos-python\get_images\file.txt", True)
    a.WriteLine (ThisWorkbook.FullName)
    a.WriteLine ("4" & vbNewLine & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("AO41") & vbNewLine & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q43") & vbNewLine & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q44"))
    a.Close

    Call Shell("cmd.exe /S /C" & """python C:\Users\noliveira\Documents\automatizacao-laudos-python\get_images\main.py""", vbNormalFocus)
    
    
     With ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("AO41")
        .Value = .Value + 1
    End With
    
End Sub

Sub DownloadImage5()
    Set fs = CreateObject("Scripting.FileSystemObject")
    Set a = fs.CreateTextFile("C:\Users\noliveira\Documents\automatizacao-laudos-python\get_images\file.txt", True)
    a.WriteLine (ThisWorkbook.FullName)
    a.WriteLine ("5" & vbNewLine & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("AO59") & vbNewLine & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q61") & vbNewLine & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q62"))
    a.Close

    Call Shell("cmd.exe /S /C" & """python C:\Users\noliveira\Documents\automatizacao-laudos-python\get_images\main.py""", vbNormalFocus)
    
    
     With ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("AO59")
        .Value = .Value + 1
    End With
    
End Sub

Sub DownloadImage6()
    Set fs = CreateObject("Scripting.FileSystemObject")
    Set a = fs.CreateTextFile("C:\Users\noliveira\Documents\automatizacao-laudos-python\get_images\file.txt", True)
    a.WriteLine (ThisWorkbook.FullName)
    a.WriteLine ("6" & vbNewLine & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("AO71") & vbNewLine & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q73") & vbNewLine & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q74"))
    a.Close

    Call Shell("cmd.exe /S /C" & """python C:\Users\noliveira\Documents\automatizacao-laudos-python\get_images\main.py""", vbNormalFocus)
    
    
     With ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("A071")
        .Value = .Value + 1
    End With
    
End Sub

Sub UpdatePic1()
    Dim imagePath As String
    Dim folder As String
    Dim imagePath2 As String
    Dim a As Variant
    
    imagePath = ActiveWorkbook.Path
    a = Split(imagePath, "/")
    
    folder = "C:\Users\noliveira\Empírica Investimentos Gestão de Recursos Ltda\ESCO - Documentos\5 - Avaliacoes de Imoveis\Keycash\" + a(8) + "\" + a(9)
    imagePath2 = folder + "\img\amostra1.png"
    
    ActiveSheet.Pictures.Insert imagePath2
End Sub

Sub UpdatePic2()
    Dim imagePath As String
    Dim folder As String
    Dim imagePath2 As String
    Dim a As Variant
    
    imagePath = ActiveWorkbook.Path
    a = Split(imagePath, "/")
    
    folder = "C:\Users\noliveira\Empírica Investimentos Gestão de Recursos Ltda\ESCO - Documentos\5 - Avaliacoes de Imoveis\Keycash\" + a(8) + "\" + a(9)
    imagePath2 = folder + "\img\amostra2.png"
    
    ActiveSheet.Pictures.Insert imagePath2

End Sub

Sub UpdatePic3()
    Dim imagePath As String
    Dim folder As String
    Dim imagePath2 As String
    Dim a As Variant
    
    imagePath = ActiveWorkbook.Path
    a = Split(imagePath, "/")
    
    folder = "C:\Users\noliveira\Empírica Investimentos Gestão de Recursos Ltda\ESCO - Documentos\5 - Avaliacoes de Imoveis\Keycash\" + a(8) + "\" + a(9)
    imagePath2 = folder + "\img\amostra3.png"
    
    ActiveSheet.Pictures.Insert imagePath2

End Sub

Sub UpdatePic4()
    Dim imagePath As String
    Dim folder As String
    Dim imagePath2 As String
    Dim a As Variant
    
    imagePath = ActiveWorkbook.Path
    a = Split(imagePath, "/")
    
    folder = "C:\Users\noliveira\Empírica Investimentos Gestão de Recursos Ltda\ESCO - Documentos\5 - Avaliacoes de Imoveis\Keycash\" + a(8) + "\" + a(9)
    imagePath2 = folder + "\img\amostra4.png"
    
    ActiveSheet.Pictures.Insert imagePath2

End Sub

Sub UpdatePic5()
    Dim imagePath As String
    Dim folder As String
    Dim imagePath2 As String
    Dim a As Variant
    
    imagePath = ActiveWorkbook.Path
    a = Split(imagePath, "/")
    
    folder = "C:\Users\noliveira\Empírica Investimentos Gestão de Recursos Ltda\ESCO - Documentos\5 - Avaliacoes de Imoveis\Keycash\" + a(8) + "\" + a(9)
    imagePath2 = folder + "\img\amostra5.png"
    
    ActiveSheet.Pictures.Insert imagePath2

End Sub

Sub UpdatePic6()
    Dim imagePath As String
    Dim folder As String
    Dim imagePath2 As String
    Dim a As Variant
    
    imagePath = ActiveWorkbook.Path
    a = Split(imagePath, "/")
    
    folder = "C:\Users\noliveira\Empírica Investimentos Gestão de Recursos Ltda\ESCO - Documentos\5 - Avaliacoes de Imoveis\Keycash\" + a(8) + "\" + a(9)
    imagePath2 = folder + "\img\amostra6.png"
    
    ActiveSheet.Pictures.Insert imagePath2

End Sub

Sub DownloadMap()
    Set fs = CreateObject("Scripting.FileSystemObject")
    Set a = fs.CreateTextFile("C:\Users\noliveira\Documents\automatizacao-laudos-python\get_map\file.txt", True)
    a.WriteLine (ThisWorkbook.FullName)
    a.WriteLine (ThisWorkbook.Worksheets("Modelo de Laudo").Range("E22") & " " & ThisWorkbook.Worksheets("Modelo de Laudo").Range("Q22") & ", " & ThisWorkbook.Worksheets("Modelo de Laudo").Range("E23") & ", " & ThisWorkbook.Worksheets("Modelo de Laudo").Range("E24"))
    a.Close

    Call Shell("cmd.exe /S /C" & """python C:\Users\noliveira\Documents\automatizacao-laudos-python\get_map\main.py""", vbNormalFocus)
End Sub

Sub DownloadMapSamples()
    Set fs = CreateObject("Scripting.FileSystemObject")
    Set a = fs.CreateTextFile("C:\Users\noliveira\Documents\automatizacao-laudos-python\get_map\file.txt", True)
    a.WriteLine (ThisWorkbook.FullName)
    a.WriteLine (ThisWorkbook.Worksheets("Modelo de Laudo").Range("E22") & " " & ThisWorkbook.Worksheets("Modelo de Laudo").Range("Q22") & ", " & ThisWorkbook.Worksheets("Modelo de Laudo").Range("E23") & ", " & ThisWorkbook.Worksheets("Modelo de Laudo").Range("E24"))
    a.WriteLine (ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q7") & ", " & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q8") & ", " & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("AB8"))
    a.WriteLine (ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q19") & ", " & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q20") & ", " & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("AB20"))
    a.WriteLine (ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q31") & ", " & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q32") & ", " & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("AB32"))
    a.WriteLine (ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q43") & ", " & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q44") & ", " & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("AB44"))
    a.WriteLine (ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q61") & ", " & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q62") & ", " & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("AB62"))
    a.WriteLine (ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q73") & ", " & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("Q74") & ", " & ThisWorkbook.Worksheets("Pesquisa de Mercado").Range("AB74"))
    a.Close

    Call Shell("cmd.exe /S /C" & """python C:\Users\noliveira\Documents\automatizacao-laudos-python\get_map\main.py""", vbNormalFocus)
End Sub

Sub ImportMap()
    Dim ws As Worksheet
    Dim imagePath As String
    Dim folder As String
    Dim imagePath2 As String
    Dim a As Variant
    Dim img As Picture
    Set ws = Worksheets("Descrição")
    
    imagePath = ActiveWorkbook.Path
    
    a = Split(imagePath, "/")
    folder = "C:\Users\noliveira\Empírica Investimentos Gestão de Recursos Ltda\ESCO - Documentos\5 - Avaliacoes de Imoveis\Keycash\" + a(8) + "\" + a(9)
    imagePath2 = folder + "\img\map.png"
    Set img = ws.Pictures.Insert(imagePath2)
    
    With img
        .ShapeRange.LockAspectRatio = True
        .Width = 500

    End With

End Sub

Sub ImportMapSamples()
    Dim ws As Worksheet
    Dim imagePath As String
    Dim folder As String
    Dim imagePath2 As String
    Dim a As Variant
    Dim img As Picture
    Set ws = Worksheets("Pesquisa de Mercado")
    
    imagePath = ActiveWorkbook.Path
    
    a = Split(imagePath, "/")
    folder = "C:\Users\noliveira\Empírica Investimentos Gestão de Recursos Ltda\ESCO - Documentos\5 - Avaliacoes de Imoveis\Keycash\" + a(8) + "\" + a(9)
    imagePath2 = folder + "\img\map.png"
    
    Set img = ws.Pictures.Insert(imagePath2)
    
    With img
        .ShapeRange.LockAspectRatio = True
        .Width = 500

    End With

End Sub

Sub SearchDistances()
    Set fs = CreateObject("Scripting.FileSystemObject")
    Set a = fs.CreateTextFile("C:\Users\noliveira\Documents\automatizacao-laudos-python\get_distances\file.txt", True)
    a.WriteLine (ThisWorkbook.FullName)
    a.WriteLine (ThisWorkbook.Worksheets("Modelo de Laudo").Range("E22") & " " & ThisWorkbook.Worksheets("Modelo de Laudo").Range("Q22") & ", " & ThisWorkbook.Worksheets("Modelo de Laudo").Range("E23") & ", " & ThisWorkbook.Worksheets("Modelo de Laudo").Range("E24"))
    a.Close

    Call Shell("cmd.exe /S /C" & """python C:\Users\noliveira\Documents\automatizacao-laudos-python\get_distances\main.py""", vbNormalFocus)
End Sub

Sub ImportDistances()
    Dim OpenBook As Workbook
    Dim DataFile As String
    Dim folder As String
    Dim DataFile2 As String
    Dim a As Variant
    Dim i As Integer
    
    DataFile = ActiveWorkbook.Path
    
    a = Split(DataFile, "/")
    folder = "C:/Users/noliveira/Empírica Investimentos Gestão de Recursos Ltda/ESCO - Documentos/5 - Avaliacoes de Imoveis/Keycash/" + a(8) + "/" + a(9)
    DataFile2 = folder + "/locais_coletados.xlsx"
    
    If a(0) = "https:" Then
        Set OpenBook = Application.Workbooks.Open(DataFile2)
    Else
        Set OpenBook = Application.Workbooks.Open(DataFile + "/locais_coletados.xlsx")
    End If
    
    Range("D46:AH55").Select
    Application.CutCopyMode = False
    Selection.ClearContents
    
    For i = 2 To 12
        ThisWorkbook.Worksheets("Descrição").Cells(44 + i, 4).Value = OpenBook.Sheets(1).Cells(i, 2).Value
        ThisWorkbook.Worksheets("Descrição").Cells(44 + i, 28).Value = OpenBook.Sheets(1).Cells(i, 3).Value
    Next i

    OpenBook.Close False
    
    Application.ScreenUpdating = True
    
End Sub

