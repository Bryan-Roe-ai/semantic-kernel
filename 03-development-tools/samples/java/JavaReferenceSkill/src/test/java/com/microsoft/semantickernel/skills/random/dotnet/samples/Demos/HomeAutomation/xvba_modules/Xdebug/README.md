# Xdebug (VBA Immediate Window in Output VSCode Window)
    
## Description
 - This package provides a way to simulate VBA Immediate Window in Output VSCode window
 - Find the Output window (VBA Immediate Window)

 ## Methods

 <p>
<img src="https://github.com/Aeraphe/xdebug/blob/main/images/immediate.gif" alt="VBA immediate Window">
</p>


 ### Xdebug.printx

- This method print any type os variable


```

Public Sub index()


  Dim test(1) As Variant

  'Add an Object
  Set test(0) = Sheets(1)
  'Add a String
  test(1) = "Test Xdebug Output"
  
  Xdebug.printx test

End Sub

```


 ### Xdebug.printError

- This method is use for print error


```
 Public Sub index()
  
  On Error GoTo ErrorHandle:
    'throw an error
    d = 1/0
    'Your code here
  
  
 ErrorHandle:
    Xdebug.errorSource = "pageConsoller.index"
    Xdebug.printError

 End Sub
```



---

## 👨‍💻 Author & Attribution

**Created by Bryan Roe**  
Copyright (c) 2025 Bryan Roe  
Licensed under the MIT License

This is part of the Semantic Kernel - Advanced AI Development Framework.
For more information, see the main project repository.
