from sklearn import svm, metrics
import glob, os.path, re, json

#os.path 경로 찾을때 폴더에 있는 파일들 가져올때
#glob 경로에 있는 파일들을 불러올때 사용하는거
#re는 정규식 패턴을 읽어서 파일 불러오는것들
#json 데이터로 저장했다는것

#텍스트를 읽어 들이고 출현 빈도 조사하기
def check_freq(fname):
    name = os.path.basename(fname) #경로 (/home/ssam/PycharmProjects/BasicPython/lang/train/en-1.txt)
    # re.match(r'[a-z]{2}\-[0-9]+')
    # 뒤에 정규표현식 설명받아야됨 re.match(r'^[a-z]{2}[0-9]$')  // [0-9]$달러는 숫자로 끝난다를 의미 역슬레쉬는\ 특수기호
    #match 그거와 일치하는걸 찾으면 true 즉 다른나라어와 일치하는걸 찾으면 매치된 객체와 리턴해줌
    # 문서의 정답
    lang = re.match(r'^[a-z]{2,}', name).group()
    with open(fname, 'r', encoding='utf-8') as f:
        #문제
        text = f.read()

    text = text.lower()
    #a를 0으로 z를 25로 하는 숫자로 바꿔주는것
    cnt = [0 for n in range(0,26)] #count 변수에 배열
    code_a = ord('a') # -> 97
    code_z = ord('z') # -> 122

    #알파벳 출현 횟수 구하기
    for ch in text:
        n = ord(ch)
        if code_a <= n <= code_z:
            cnt[n-code_a] += 1

    #정규화하기
    total = sum(cnt)
    # Java 8이상부터 사용 가능한 Stream API
    # cnt.stream().map(x -> x/ total).collect(Collections.toList); 자바식 표현
    # for index in range(0, 26):
    #     cnt[index] = cnt[index] / total
    freq = list(map(lambda x: x / total,cnt ))

    return freq, lang

# 각 파일 처리하기
def load_files(path):
    freqs = []
    labels =[]
    file_list = glob.glob(path)
    for fname in file_list:
        r = check_freq(fname)
        freqs.append(r[0])
        labels.append(r[1])
    return  {"freqs": freqs, 'labels' : labels}

train = load_files('train/*.txt')
test = load_files('test/*.txt')

with open('freq.json', 'w', encoding='utf-8') as f:
    json.dump([train, test], f)

train_X = train['freqs']
train_y = train['labels']
test_X = test['freqs']
test_y = test['labels']

#학습하기
clf = svm.SVC()
clf.fit(train_X,train_y)

pred = clf.predict(test_X)

#결과확인
accuracy_score = metrics.accuracy_score(test_y, pred)
print(f'정답률: {accuracy_score}' )
cls_report = metrics.classification_report(test_y,pred)
print(f'리포트\n {cls_report}')

