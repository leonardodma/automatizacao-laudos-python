Function Username() As String
    Username = Environ("Username")
End Function

Sub DownloadMap()
    Set fs = CreateObject("Scripting.FileSystemObject")
    Set a = fs.CreateTextFile("C:\Users\" + Username() + "\Documents\automatizacao-laudos-python\get_map\file.txt", True)
    a.WriteLine (ThisWorkbook.FullName)
    a.WriteLine (ThisWorkbook.Worksheets("Modelo de Laudo").Range("E21") & " " & ThisWorkbook.Worksheets("Modelo de Laudo").Range("M22") & ", " & ThisWorkbook.Worksheets("Modelo de Laudo").Range("E22") & ", " & ThisWorkbook.Worksheets("Modelo de Laudo").Range("E23"))
    a.Close

    Call Shell("cmd.exe /S /C" & """python C:\Users\" + Username() + "\Documents\automatizacao-laudos-python\get_map\main.py""", vbNormalFocus)
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
    folder = "C:\Users\" + Username() + "\Empírica Investimentos Gestão de Recursos Ltda\ESCO - Documentos\5 - Avaliacoes de Imoveis\Laudos Creditas\" + a(8) + "\" + a(9)
    imagePath2 = folder + "\img\map.png"
    Set img = ws.Pictures.Insert(imagePath2)
    
    With img
        .ShapeRange.LockAspectRatio = True
        .Width = 500

    End With

End Sub

Sub GetSamples()
    Set fs = CreateObject("Scripting.FileSystemObject")
    Set a = fs.CreateTextFile("C:\Users\" + Username() + "\Documents\automatizacao-laudos-python\get_data\file.txt", True)
    a.WriteLine (ThisWorkbook.FullName)

    'Endereco
    a.WriteLine (ThisWorkbook.Worksheets("Modelo de Laudo").Range("E21"))
    'numero
    a.WriteLine (ThisWorkbook.Worksheets("Modelo de Laudo").Range("M22"))
    'bairro
    a.WriteLine (ThisWorkbook.Worksheets("Modelo de Laudo").Range("E22"))
    'municipio
    a.WriteLine (ThisWorkbook.Worksheets("Modelo de Laudo").Range("E23"))
    'uf
    a.WriteLine (ThisWorkbook.Worksheets("Modelo de Laudo").Range("V23"))
    'CEP
    a.WriteLine (ThisWorkbook.Worksheets("Modelo de Laudo").Range("M23"))
    'tipo
    a.WriteLine (ThisWorkbook.Worksheets("Modelo de Laudo").Range("F26"))
    'area
    a.WriteLine (ThisWorkbook.Worksheets("Modelo de Laudo").Range("G34"))
    a.Close
    
    Call Shell("cmd.exe /S /K" & """python C:\Users\" + Username() + "\Documents\automatizacao-laudos-python\get_data\main.py""", vbNormalFocus)

End Sub

Sub ImportSamples()
    Dim OpenBook As Workbook
    Dim DataFile As String
    Dim folder As String
    Dim DataFile2 As String
    Dim a As Variant
    
    DataFile = ActiveWorkbook.Path
    
    a = Split(DataFile, "/")
    folder = "C:/Users/" + Username() + "/Empírica Investimentos Gestão de Recursos Ltda/ESCO - Documentos/5 - Avaliacoes de Imoveis/Laudos Creditas/" + a(8) + "/" + a(9)
    DataFile2 = folder + "/dados_coletados.xlsx"
    
    If a(0) = "https:" Then
        Set OpenBook = Application.Workbooks.Open(DataFile2)
    Else
        Set OpenBook = Application.Workbooks.Open(DataFile + "/dados_coletados.xlsx")
    End If
    
    OpenBook.Sheets(1).Range("A1").CurrentRegion.Copy
    ThisWorkbook.Worksheets("Amostras").Range("D1").PasteSpecial xlPasteValues
    OpenBook.Close False
    
    Application.ScreenUpdating = True
    
End Sub

Sub CreateShortcut()
    Application.OnKey "+^{Q}", "AjustaImagens"
End Sub

Sub AjustaImagens()
    Dim sh As Shape

    For Each sh In ActiveSheet.Shapes
    If sh.Name Like "*Pict*" And sh.TopLeftCell.Row > 6 Then
        ActiveSheet.Shapes.Range(Array(sh.Name)).Select
            With Selection
            If .ShapeRange.Height > .ShapeRange.Width Then
            .ShapeRange.Height = sh.TopLeftCell.MergeArea.Height - 8
            End If
            If .ShapeRange.Width >= .ShapeRange.Height Then
            .ShapeRange.Width = sh.TopLeftCell.MergeArea.Width - 8
            End If
            .Left = sh.TopLeftCell.MergeArea.Left + ((sh.TopLeftCell.MergeArea.Width - sh.Width) / 2)
            .Top = sh.TopLeftCell.MergeArea.Top + ((sh.TopLeftCell.MergeArea.Height - sh.Height) / 2)
            End With
    End If
    Next

End Sub