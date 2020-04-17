실행파일은 gitvim.py로 git repository 내부에 설치하여 실행한다

실행방법
cd (git repository 이름)
python gitvim.py (찾고싶은 파일 부분이름 or Regular Expression)

그냥 file name중 일부를 넣거나, regular expression 을 넣는 게 모두 가능하다.
예시1) python gitvim.py "(b|m|a|i|c)le" (b,m,a,i,c중 하나 이상을 포함하면서 le가 오는경우) (regular expression)
test_luna/make_clean.sh (1)
test_luna/test_profiler.lua (2)
test_luna/test_simple.lua (3)
가 출력 되는 것을 확인할 수 있다.
예시2) python gitvim.py luna
등이 있으며 이후 output이 여러개인 경우 파일 명의 일부나, 해당 숫자를 통해 구체화 시키거나 파일을
실행 시킬 수 있다.

코드의 간단한 설명으로는 git 디렉토리 내부의 파일 이름들을 childOutput에 저장하여
applicants에 해당 이름의 일부가 있거나 RE인 경우 저장한다
0개일 경우 없다는 출력, 1개일 경우 해당 파일을 실행하고
이외의 경우에는 applicants를 출력한다. 이후 그 applicants 내부에서 다시 정하거나 골라 applicants를 최신화한다.
파일이 실행되거나 없을 경우 이후 while문을 모두 빠져나와 종료한다.