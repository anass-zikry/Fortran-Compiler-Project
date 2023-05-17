# Compilers CFG

1. ProgramStart ➡️ ProgramUnit ProgramStart2 
2. ProgramStart2 ➡️ ProgramUnit ProgramStart2 | ɜ
3. ProgramUnit ➡️ Header Block Footer
4. Header ➡️ program identifier delimiter
5. Block ➡️ implicit none delimiter TypeDecls Statements
6. Footer ➡️ end program identifier delimiter
7. TypeDecls ➡️ TypeDecl TypeDecls2 | ɜ 
8. TypeDecls2 ➡️ TypeDecl TypeDecls2 | ɜ
9. TypeDecl ➡️ DataType TypeDecl2
10. TypeDecl2 ➡️ :: IdentifierList delimiter | , parameter :: NamedConstant delimiter
11. DataType ➡️ integer | real | complex | logical | CharacterDType
12. NamedConstant ➡️ identifier = LogicalOrConst
13. CharacterDType ➡️ character CharacterDType2
14. CharacterDType2 ➡️ ( len = IdorConst) | ɜ
15. Statements ➡️ Statement Statements2 
16. Statements2 ➡️ Statement Statements2 | ɜ
17. Statement ➡️ Assignment | Print | Read | IF | DoLoop | ɜ 
18. Assignment ➡️ identifier = Relations delimiter
19. Relations ➡️ IdorConst Relation | LogicalVal
20. Relation ➡️ ArithmeticOp IdorConst Relation2 | ɜ
21. Relation2 ➡️ ArithmeticOp IdorConst Relation2 | ɜ
22. Print ➡️ print *  PrintCall delimiter
23. PrintCall ➡️ , PrintList | ɜ
24. PrintList ➡️ PrintHolder PrintList2 
25. PrintList2 ➡️ , PrintHolder PrintList2 | ɜ
26. PrintHolder ➡️ identifier | constant | string | ɜ
27. Read ➡️ read * , IdentifierList delimiter
28. IF ➡️ IFStart IF2
29. IF2 ➡️ end if delimiter | else delimiter Statements end if delimiter
30. IFStart ➡️ if Conditional then delimiter Statements
31. DoLoop ➡️ DoStart Statements end do delimiter
32. DoStart ➡️ do identifier = constant , IdorConst  Step delimiter
33. Step ➡️ , IdorConst  | ɜ
34. ArithmeticOp ➡️ * | / | + | -
35. IdentifierList ➡️ identifier IdentifierList2 
36. IdentifierList2 ➡️ , identifier IdentifierList2 | ɜ
37. Conditional ➡️ IdorConst RelationalOp IdorConst | identifier | LogicalVal
38. IdorConst ➡️ identifier | constant
39. RelationalOp ➡️ > | < | <= | >= | == | /= 
40. LogicalOrIdentifier ➡️ LogicalVal | IdentifierList
41. LogicalOrConst ➡️ LogicalVal | constant
42. LogicalVal ➡️ true | false