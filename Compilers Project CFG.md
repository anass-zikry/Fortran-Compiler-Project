# Compilers CFG

1. ProgramStart ➡️ ProgramUnit ProgramStart2 
2. ProgramStart2 ➡️ ProgramUnit ProgramStart2 | ɛ
3. ProgramUnit ➡️ Header Block Footer
4. Header ➡️ program identifier delimiter
5. Block ➡️ implicit none delimiter TypeDecls Statements
6. Footer ➡️ end program identifier delimiter
7. TypeDecls ➡️ TypeDecl TypeDecls2 | ɛ
8. TypeDecls2 ➡️ TypeDecl TypeDecls2 | ɛ
9. TypeDecl ➡️ DataType TypeDecl2
10. TypeDecl2 ➡️ :: IdentifierList delimiter | , parameter :: NamedConstant delimiter
11. DataType ➡️ integer | real | complex | logical | CharacterDType
12. NamedConstant ➡️ identifier = NamedConstant2 
13. NamedConstant2➡️ LogicalOrConst | ComplexNotation 
14. CharacterDType ➡️ character CharacterDType2
15. CharacterDType2 ➡️ ( len = IdorConst) | ɛ 
16. Statements ➡️ Statement Statements2 
17. Statements2 ➡️ Statement Statements2 | ɛ
18. Statement ➡️ Assignment | Print | Read | IF | DoLoop | ɛ
19. Assignment ➡️ identifier = Relations delimiter
20. Relations ➡️ Expression | LogicalVal | ComplexNotation 🍎
21. Expression➡️ MultTerm Expression2
22. Expression2 ➡️ AddOp MultTerm Expression2 | ɛ
23. MultTerm➡️ IdorConst MultTerm2
24. MultTerm2 ➡️ MultOp IdorConst MultTerm2 | ɛ
25. Relation ➡️ ArithmeticOp IdorConst Relation2 | ɛ 💀 
26. Relation2 ➡️ ArithmeticOp IdorConst Relation2 | ɛ 💀
27. Print ➡️ print *  PrintCall delimiter
28. PrintCall ➡️ , PrintList | ɛ
29. PrintList ➡️ PrintHolder PrintList2 
30. PrintList2 ➡️ , PrintHolder PrintList2 | ɛ
31. PrintHolder ➡️ identifier | constant | string | ɛ
32. Read ➡️ read * , IdentifierList delimiter
33. IF ➡️ IFStart IF2
34. IF2 ➡️ end if delimiter | else delimiter Statements end if delimiter
35. IFStart ➡️ if ( Conditional ) then delimiter Statements
36. DoLoop ➡️ DoStart Statements end do delimiter
37. DoStart ➡️ do identifier = constant , IdorConst  Step delimiter
38. Step ➡️ , IdorConst  | ɛ
39. ArithmeticOp ➡️ * | / | + | - 💀
40. MultOp➡️ * | /
41. AddOp➡️ + | -
42. IdentifierList ➡️ identifier IdentifierList2 
43. IdentifierList2 ➡️ , identifier IdentifierList2 | ɛ
44. Conditional ➡️ Expression RelationalOp Expression | identifier | LogicalVal 🍎
45. ComplexNotation➡️ ( NegorPos real , NegorPos real )
46. IdorConst ➡️ NegorPos IdorConst2 
47. IdorConst2 ➡️ identifier | constant 
48. RelationalOp ➡️ > | < | <= | >= | == | /= 
49. LogicalOrIdentifier ➡️ LogicalVal | IdentifierList
50. LogicalOrConst ➡️ LogicalVal | constant
51. LogicalVal ➡️ true | false
52. NegorPos ➡️ - | + | ɛ 

BooleanExp➡️ Exp BooleanOp Exp