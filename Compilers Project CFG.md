# Compilers CFG

1. ProgramStart ➡️ ProgramUnit ProgramStart2  
2. ProgramStart2 ➡️ ProgramUnit ProgramStart2 | ɛ
3. ProgramUnit ➡️ Header Block Footer
4. Header ➡️ program identifier
5. Block ➡️ implicit none TypeDecls Statements
6. Footer ➡️ end program identifier
7. TypeDecls ➡️ TypeDecl TypeDecls2 | ɛ 
8. TypeDecls2 ➡️ TypeDecl TypeDecls2 | ɛ
9. TypeDecl ➡️ DataType TypeDecl2
10. TypeDecl2 ➡️ :: IdentifierList | , parameter :: NamedConstant
11. DataType ➡️ integer | real | complex | logical | CharacterDType
12. NamedConstant ➡️ identifier = LogicalOrConst
13. CharacterDType ➡️ character CharacterDType2
14. CharacterDType2 ➡️ ( len = IdorConst) | ɛ
15. Statements ➡️ Statement Statements2 
16. Statements2 ➡️ Statement Statements2 | ɛ
17. Statement ➡️ Assignment | Print | Read | If | DoLoop | ɛ 
18. Assignment ➡️ identifier = Relations
19. Relations ➡️ IdorConst Relation | LogicalVal
20. Relation ➡️ ArithmeticOp IdorConst Relation2 | ɛ
21. Relation2 ➡️ ArithmeticOp IdorConst Relation2 | ɛ
22. Print ➡️ print *  PrintCall
23. PrintCall ➡️ , PrintList | ɛ
24. PrintList ➡️ PrintHolder PrintList2 
25. PrintList2 ➡️ , PrintHolder PrintList2 | ɛ
26. PrintHolder ➡️ identifier | constant | string | ɛ
27. Read ➡️ read * , IdentifierList
28. If ➡️ IfStart If2
29. If2 ➡️ end if | else Statements end if
30. IfStart ➡️ if ( Conditional ) then Statements 
31. DoLoop ➡️ DoStart Statements end do
32. DoStart ➡️ do identifier = IdorConst , IdorConst  Step
33. Step ➡️ , IdorConst  | ɛ
34. ArithmeticOp ➡️ * | / | + | -
35. IdentifierList ➡️ identifier IdentifierList2 
36. IdentifierList2 ➡️ , identifier IdentifierList2 | ɛ
37. Conditional ➡️ IdorConst RelationalOp IdorConst | identifier | LogicalVal🍎 
38. IdorConst ➡️ identifier | constant
39. RelationalOp ➡️ > | < | <= | >= | == | /= 
40. LogicalOrIdentifier ➡️ LogicalVal | IdentifierList
41. LogicalOrConst ➡️ LogicalVal | constant
42. LogicalVal ➡️ true | false