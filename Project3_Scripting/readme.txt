���������� gitvim.py�� git repository ���ο� ��ġ�Ͽ� �����Ѵ�

������
cd (git repository �̸�)
python gitvim.py (ã����� ���� �κ��̸� or Regular Expression)

�׳� file name�� �Ϻθ� �ְų�, regular expression �� �ִ� �� ��� �����ϴ�.
����1) python gitvim.py "(b|m|a|i|c)le" (b,m,a,i,c�� �ϳ� �̻��� �����ϸ鼭 le�� ���°��) (regular expression)
test_luna/make_clean.sh (1)
test_luna/test_profiler.lua (2)
test_luna/test_simple.lua (3)
�� ��� �Ǵ� ���� Ȯ���� �� �ִ�.
����2) python gitvim.py luna
���� ������ ���� output�� �������� ��� ���� ���� �Ϻγ�, �ش� ���ڸ� ���� ��üȭ ��Ű�ų� ������
���� ��ų �� �ִ�.

�ڵ��� ������ �������δ� git ���丮 ������ ���� �̸����� childOutput�� �����Ͽ�
applicants�� �ش� �̸��� �Ϻΰ� �ְų� RE�� ��� �����Ѵ�
0���� ��� ���ٴ� ���, 1���� ��� �ش� ������ �����ϰ�
�̿��� ��쿡�� applicants�� ����Ѵ�. ���� �� applicants ���ο��� �ٽ� ���ϰų� ��� applicants�� �ֽ�ȭ�Ѵ�.
������ ����ǰų� ���� ��� ���� while���� ��� �������� �����Ѵ�.