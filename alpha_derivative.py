from sympy import *
x, y, yp, c = symbols('x y yp c')  # dy/dx꼴의 미분을 지원합니다. 적분상수는 c입니다.

def divide_val_derivative(eq):  # eq type : string
    threeWordsFunc = ['exp', 'sin', 'cos', 'tan', 'csc', 'sec', 'cot']  # 함수 자체가 괄호로 이루어진 경우 문자열 분석 예외처리
    eq_bak = eq
    position = 0  # position: dy/dx 위치 저장하는 변수. 좌변이면 0, 우변이면 1
    yp_location = eq.index("yp")  # dy/dx 위치 찾기
    equal_location = eq.index("=")  # 등호 위치 찾기
    if yp_location < equal_location:
        position = 0  # dy/dx가 좌변에 있으면 position = 0
    else:
        position = 1  # 우변에 dy/dx가 있으면 position = 1
    del yp_location  # position 나왔으면 이제 필요 없음
    del equal_location  # position 나왔으면 이제 필요 없음
    eq = eq.split("=")  # eq = [좌변(string),우변(string)]

    # 수식 괄호로 항 분석
    eqa = [[], []]  # 지수 부분 제외하고 항 분리한 수식들 위치를 괄호의 위치를 통해 넣는 list
    eqa_exponential = [[], []]  # 항 분리한 수식들 중 지수 부분의 위치를 괄호의 위치를 통해 넣는 list
    # 좌변 processing
    bracket = 0  # 괄호 갯수 카운트 위한 변수.
    bracket_mode = 0  # 지수 부분인지 중괄호로 판독하는 용도. 중괄호 갯수 기록.
    for i in range(len(eq[0])):
        if eq[0][i] == '{':
            if bracket_mode == 0:
                eqa_exponential[0].append(i)
            bracket_mode += 1
        elif eq[0][i] == '}':
            bracket_mode -= 1
            if bracket_mode == 0:
                eqa_exponential[0].append(i)
        if eq[0][i] == "(" and not(bracket_mode):  # 괄호가 열리면
            if bracket == 0:  # 가장 바깥쪽 괄호의 시작 부분
                eqa[0].append(i)
            bracket += 1
        elif eq[0][i] == ")" and not(bracket_mode):  # 괄호가 닫히면
            bracket -= 1
            if bracket == 0:  # 가장 바깥쪽 괄호가 끝나는 부분
                eqa[0].append(i)
    if bracket != 0: raise Exception('좌변의 괄호를 제대로 구성하지 않았습니다.')
    if eq[0] == '0': eqa[0].append(0) #0이라서 아무것도 입력되지 않은 경우
    elif len(eqa[0]) == 0: eqa[0][0] = eq[0] #항이 1개 있어서 괄호를 작성하지 않은 경우.

    # 우변 processing
    bracket = 0  # 괄호 갯수 카운트 위한 변수.
    bracket_mode = 0  # 지수 부분인지 중괄호로 판독하는 용도. 0이 아니면 중괄호 안에서 탐색(=지수 부분)하고 있다는 뜻.
    for i in range(len(eq[1])):
        if eq[1][i] == '{':
            if bracket_mode == 0:
                eqa_exponential[1].append(i)
            bracket_mode += 1
        elif eq[1][i] == '}':
            bracket_mode -= 1
            if bracket_mode == 0:
                eqa_exponential[1].append(i)
        if eq[1][i] == "(" and not(bracket_mode):  # 괄호가 열리면
            if bracket == 0:  # 가장 바깥쪽 괄호의 시작 부분
                eqa[1].append(i)
            bracket += 1
        elif eq[1][i] == ")" and not(bracket_mode):  # 괄호가 닫히면
            bracket -= 1
            if bracket == 0:  # 가장 바깥쪽 괄호가 끝나는 부분
                eqa[1].append(i)
    if bracket != 0: raise Exception('우변의 괄호를 제대로 구성하지 않았습니다.')
    if eq[1] == '0': eqa[1].append(0) #0이라서 아무것도 입력되지 않은 경우
    elif len(eqa[1]) == 0: eqa[1][0] = eq[1]  # 항이 1개 있어서 괄호를 작성하지 않은 경우.

    bracket_sign = [[], []]  # 괄호가 어떤 사칙연산 기호로 분리되어 있는지 check. plus, minus, multi, divide 4가지로 구분.
    term_data = [[], []]  # 괄호로 분리된 부분을 각각 저장하는 list.
    dydxlocation = []
    # 괄호 데이터 토대로 항 분리 및, dy/dx 탐지

    # 좌변 프로세싱
    for i in range(0, len(eqa[0]), 2):
        if eq[0][eqa[0][i]-3:eqa[0][i]] in threeWordsFunc:
            term = eq[0][eqa[0][i]-3:eqa[0][i + 1] + 1]  # sin(x)같이 괄호 앞 3글자까지 추출해야 하는 경우에 대응.
            if 'yp' in term:
                dydxlocation = [1, int(i / 2), term.index('yp')]  # dydxlocation 형식: [좌변: 0 우변: 1, 몇 번째 괄호로 나뉜 부분에 있는지, 항 안의 어디 부분에 있는지]
            if i == 0: #변의 맨 처음 부분일 경우
                bracket_sign[0].append('plus')
            elif eq[0][eqa[0][i] - 4] == '+':  # 괄호 앞에 + 있으면
                bracket_sign[0].append('plus')
            elif eq[0][eqa[0][i] - 4] == '-':  # 괄호 앞에 - 있으면
                bracket_sign[0].append('minus')
            elif eq[0][eqa[0][i] - 4] in ['*',')']:  # 괄호 앞에 * 있거나, 닫힌 괄호로 곱셈이라는 표기가 있으면
                bracket_sign[0].append('multi')
            elif eq[0][eqa[0][i] - 4] == '/':  # 괄호 앞에 / 있으면
                bracket_sign[0].append('divide')
        else:
            if eq[0] == '0': #0밖에 없는 경우는 그냥 0으로 따로 예외처리
                bracket_sign[0].append('plus')
                term_data[0].append('(0)')
                break
            else:
                term = eq[0][eqa[0][i]:eqa[0][i + 1] + 1]  # 괄호 부분 추출
                if 'yp' in term:
                    dydxlocation = [1, int(i / 2), term.index('yp')]  # dydxlocation 형식: [좌변: 0 우변: 1, 몇 번째 괄호로 나뉜 부분에 있는지, 항 안의 어디 부분에 있는지]
                if i == 0:
                    bracket_sign[0].append('plus')  # 변의 맨 처음 부분일 경우
                elif eq[0][eqa[0][i] - 1] == '+':  # 괄호 앞에 + 있으면
                    bracket_sign[0].append('plus')
                elif eq[0][eqa[0][i] - 1] == '-':  # 괄호 앞에 - 있으면
                    bracket_sign[0].append('minus')
                elif eq[0][eqa[0][i] - 1] in ['*',')']:  # 괄호 앞에 * 있거나, 닫힌 괄호로 곱셈이라는 표기가 있으면
                    bracket_sign[0].append('multi')
                elif eq[0][eqa[0][i] - 1] == '/':  # 괄호 앞에 / 있으면
                    bracket_sign[0].append('divide')
        term_data[0].append(term)

    
    # 우변 프로세싱
    for i in range(0, len(eqa[1]), 2):
        if eq[1][eqa[1][i]-3:eqa[1][i]] in threeWordsFunc:
            term = eq[1][eqa[1][i]-3:eqa[1][i + 1] + 1]  # sin(x)같이 괄호 앞 3글자까지 추출해야 하는 경우에 대응.
            if 'yp' in term:
                dydxlocation = [1, int(i / 2), term.index('yp')]  # dydxlocation 형식: [좌변: 0 우변: 1, 몇 번째 괄호로 나뉜 부분에 있는지, 항 안의 어디 부분에 있는지]
            if i == 0: #변의 맨 처음 부분일 경우
                bracket_sign[1].append('plus')
            elif eq[1][eqa[1][i] - 4] == '+':  # 괄호 앞에 + 있으면
                bracket_sign[1].append('plus')
            elif eq[1][eqa[1][i] - 4] == '-':  # 괄호 앞에 - 있으면
                bracket_sign[1].append('minus')
            elif eq[1][eqa[1][i] - 4] in ['*',')']:  # 괄호 앞에 * 있거나, 닫힌 괄호로 곱셈이라는 표기가 있으면
                bracket_sign[1].append('multi')
            elif eq[1][eqa[1][i] - 4] == '/':  # 괄호 앞에 / 있으면
                bracket_sign[1].append('divide')
        else:
            if eq[1] == '0': #0밖에 없는 경우는 그냥 0으로 따로 예외처리
                bracket_sign[1].append('plus')
                term_data[1].append('(0)')
                break
            else:
                term = eq[1][eqa[1][i]:eqa[1][i + 1] + 1]  # 괄호 부분 추출
                if 'yp' in term:
                    dydxlocation = [1, int(i / 2), term.index('yp')]  # dydxlocation 형식: [좌변: 0 우변: 1, 몇 번째 괄호로 나뉜 부분에 있는지, 항 안의 어디 부분에 있는지]
                if i == 0:
                    bracket_sign[1].append('plus')  # 변의 맨 처음 부분일 경우
                elif eq[1][eqa[1][i] - 1] == '+':  # 괄호 앞에 + 있으면
                    bracket_sign[1].append('plus')
                elif eq[1][eqa[1][i] - 1] == '-':  # 괄호 앞에 - 있으면
                    bracket_sign[1].append('minus')
                elif eq[1][eqa[1][i] - 1] in ['*',')']:  # 괄호 앞에 * 있거나, 닫힌 괄호로 곱셈이라는 표기가 있으면
                    bracket_sign[1].append('multi')
                elif eq[1][eqa[1][i] - 1] == '/':  # 괄호 앞에 / 있으면
                    bracket_sign[1].append('divide')
        term_data[1].append(term)
    del eqa  # 처음 식 괄호 저장 데이터는 이제 필요없음
    del eqa_exponential
    del eq  # 처음 식 좌변 우변 필요없음
    del term  # 처음 수식의 항 하나하나 데이터는 이제 필요없음

    for i in range(len(term_data)):
        for j in term_data[i]:
            try:
                term_data[i][j] = term_data[i][j].replace('{', '(')
                term_data[i][j] = term_data[i][j].replace('}', ')')
                term_data[i][j] = str(factor(term_data[i][j]))
                term_data[i][j] = term_data[i][j].replace('e^', 'exp')
                term_data[i][j] = sympify(term_data[i][j])
            except: pass

    # dy/dx가 있는 변에 가서 dy/dx 항 빼고 전부 다른 변으로 이항시키기
    if len(term_data[position]) == 1: pass #dy/dx 변에 dy/dx 또는 (상수 계수)*(yp)항만 있을 경우!
    elif ('plus' not in bracket_sign[position].pop(0)) and ('minus' not in bracket_sign[position].pop(0)): #dy/dx항에 상수가 아닌 계수가 곱해져 있는 경우
        pass
    else:
        try:
            for i in range(len(term_data[position])):
                if term_data[position][i] != term_data[position][dydxlocation[1]]:  # 만약에 항이 dy/dx가 들어 있는 항이 아닐 경우
                    if bracket_sign[position][i] == 'plus':  # 원래 있던 항의 부호가 +였으면
                        term_data[not(position)].append(term_data[position][i])  # 이항
                        del term_data[position][i]
                        bracket_sign[not(position)].append('minus')
                        del bracket_sign[position][i]
                    elif bracket_sign[position][i] == 'minus':  # 원래 있던 항의 부호가 -였으면
                        term_data[not(position)].append(term_data[position][i])  # 이항
                        del term_data[position][i]
                        bracket_sign[not(position)].append('plus')
                        del bracket_sign[position][i]
                    elif bracket_sign[position][i] in ['multi','divide']: pass 
                    else:
                        print("dy/dx 변 이항 부분 오류 발생")
                        print(term_data[position])
        except IndexError: #term_data 부분에서 이항을 시키면 len(term_data[position])이 감소하므로 필히 인덱스 초과 에러 발생.
            pass
    
    # dy/dx항 반대쪽 변 항 융합 -> dy/dx 계수로 양변 나누기 -> dy/dx항 반대쪽 변 항 인수분해
    eql = [[], []]  # 최종적으로 인수분해 시킬 수식을 담는 list. 왼쪽에는 dy/dx, 오른쪽에는 나머지 항들.
    temp_eqstring = '' #dy/dx 반대쪽 변 항들을 통합할 문자열.

    if len(term_data[position]) == 1:
        eql[0] = term_data[position][0]  # dy/dx가 있는 항 대입시킴. *dy/dx 있는 변에 지금 dy/dx가 있는 항만 남아 있음. 그 전에 다른 항은 필터링해서 날려버림. +주의: dy/dx에 뭐뭐 곱해져 있는 건 여전히 남아 있음.
    elif len(term_data[position]) != 1:
        eql[0] = term_data[position]
    else:
        print('eql dy/dx 곱 에러')

    for i in range(len(term_data[not(position)])):  # term_data에 항별로 부호 분리되어 있는 애들을 부호 다시 결합시켜서 하나의 문자열로 만듦.
        if bracket_sign[not(position)][i] == 'plus':
            temp_eqstring += ("+(" + term_data[not(position)][i] + ")")
        elif bracket_sign[not(position)][i] == 'minus':
            temp_eqstring += ("-(" + term_data[not(position)][i] + ")")
        elif bracket_sign[not(position)][i] == 'multi':
            if i == 0: #아직 temp_eqstring에 아무것도 없을 때.
                temp_eqstring += ("1*(" + term_data[not(position)][i] + ")")
            else:
                temp_eqstring += ("*(" + term_data[not(position)][i] + ")")
        elif bracket_sign[not(position)][i] == 'divide':
            temp_eqstring += ("/(" + term_data[not(position)][i] + ")")
    eql[1] = '(' + temp_eqstring + ')'  # 혹시 모를 계산 우선순위 오류 방지를 위해 전체를 괄호로 감싸기
    eql[1] = str(factor(eql[1]))  # eql[1](dy/dx 반대쪽 변 수식 정리)

    del term_data  # 변수분리 전 괄호 저장한 건 이제 필요 없음. 인수분해 할 거니까 이제 무용지물.
    del bracket_sign  # 처음 수식 항들의 부호 저장한 건 이제 필요 없음. 인수분해 할 거니까 이제 무용지물.

    #dy/dx 계수로 양변을 나눠주기
    if eql[0][0] == '(' and eql[0][-1] == ')': #좌변 부분 전체가 괄호로 감싸져 있을 때는 괄호 하나를 풀어 줘서 계수가 통으로 노출될 수 있게 한다.
        eql[0] = eql[0][1:-1]
    if len(eql[0]) == 1 and eql[0] not in ['yp','(yp)']:  # dy/dx의 계수가 존재할 때.
        eql[0] = eql[0].replace('yp','1')
        eql[1] = '(' + eql[1] + ')/(1'
        if type(eql[0]) != list: #좌변 부분이 항이 가끔 1개로 나올 때.
            eql[1] += '*(' + str(factor(eql[0])) + ')'
        else:
            for i in range(len(eql[0]) - 1):
                eql[1] += '*(' + str(factor(eql[0][i])) + ')'
        eql[1] += ')'
    elif type(eql[0]) == list: #eql[0](=dy/dx 계수까지 있는 항)이 리스트 타입(=상수가 아닌 변수 계수가 있을 때)일 때
        eql[1] = '(' + eql[1] + ')'
        for i in range(len(eql[0])):
            try:
                if eql[0][i] not in ['yp', '(yp)']:
                    eql[1] += '*(1/' + str(factor(eql[0][i])) + ')'
                    del eql[0][i]
            except IndexError: pass #del 쓰니까 필히 IndexError 생길 수밖에 없음.
    eql[0] = 'yp'
    eql[1] = factor(eql[1])  # 변수분리 하기 쉽게 인수분해
    eqf = str(eql[1])  # 최종적으로 괄호 분석해서 변수분리 시킬 대상 변.
    eqf = eqf.replace(' ','')
    del eql  # 좌변은 dy/dx 뿐이고 나머지는 다 오른쪽으로 이항했으므로 이제 필요없음.
    del dydxlocation  # 좌변에 고정적으로 dy/dx만 있으므로 필요없음
    del position  # 좌변에 고정적으로 dy/dx만 있으므로 필요없음
    del temp_eqstring  # 이제 이걸로 인수분해를 끝내서 다른 곳에 옮겼으므로 필요없음.
    del bracket  # 괄호 갯수 새는 변수 일단 삭제. 나중에 필요하면 그때 다시 추가하면 됨.
    del bracket_mode #지수 인식하는 변수 일단 삭제. 나중에 필요하면 그때 다시 추가하면 됨.

    symbol_sign = [] #변수분리된 변에서 곱셈 / 나눗셈 기호 인식할 것.
    symbol_region = [] #변수분리된 변에서 곱셈 / 나눗셈 기호 위치.
    bracket = 0
    for i in range(len(eqf)):
        if eqf[i] == '(':
            bracket += 1
        elif eqf[i] == ')':
            bracket -= 1
        if (bracket == 0) and (eqf[i] in ['+', '-']): #dy/dx 빼고 나머지를 다 반대 변으로 옮겨서 인수분해했는데 곱셈꼴로 안 나오는 경우: 변수분리 불능
            print("선형미분방정식 해법을 시도하십시오.")
        elif eqf[i] == '*' and eqf[i-1] != '*' and eqf[i+1] != '*' and bracket == 0: #변수분리된 변에서 곱셈으로 되어 있어서 나눠야 할 부분!
            symbol_region.append(i)
            symbol_sign.append('multi')
        elif eqf[i] == '/' and bracket == 0: #변수분리된 변에서 나눗셈으로 되어 있어서 나눠야 할 부분!
            symbol_region.append(i)
            symbol_sign.append('divide')
    if bracket != 0: raise Exception('죄송합니다. 코딩을 제대로 못 한 제 탓입니다. 이항 이후 변수분리 과정에서 알 수 없는 오류가 발생했습니다.')

    term_data = [[], []]  # 변수분리된 변의 각 괄호 담아두는 list. 왼쪽(dy/dx 있는 변)은 y항, 오른쪽은 x항

    if len(symbol_sign) == 0: #항이 1개여서 곱셈/나눗셈 기호가 없을 때.
        term_data[1].append(eqf)
    else:
        for i in range(0, len(symbol_sign)+1):
            if i == 0: #맨 처음에
                divi_val_term = eqf[:symbol_region[i]]
            elif i != len(symbol_sign): #중간 부분
                divi_val_term = eqf[symbol_region[i-1]+1:symbol_region[i]]
            else: #맨 마지막에
                divi_val_term = eqf[symbol_region[i-1]+1:]
            term_data[1].append(divi_val_term)

    # 예외적으로 dy/dx에 다른 계수가 1개만 붙어서 eqf의 맨 오른쪽에 ~~~~/y 와 같이 괄호 없이 뚝 떨어져서 term_data에 인식되지 않은 경우
    if '/' in eqf:  # 조건1: 나눗셈 기호가 있을 것.
        if ('(' not in eqf[eqf.index('/')]) and (')' not in eqf[eqf.index('/')]):  # 여는 괄호와 닫는 괄호 둘 다 / 다음에 있지 않은 경우(괄호로 감싸지지 않은 경우)
            term_data[1].append('1/(' + eqf[eqf.index('/') + 1:] + ')')  # 나눗셈 기호(/) 바로 다음부터 전체를 항 데이터에 추가

    # 분리된 각 괄호를 분석해서 y항이 dy/dx항과 다른 변에 있으면 양변을 나눠줘서 옮김.
    for i in range(len(term_data[1])):
        try:
            if 'x' in term_data[1][i] and 'exp' not in term_data[1][i]:  # x만 위치 감지하면 exp도 감지해 버려서 예외처리
                if 'y' in term_data[1][i]:
                    print("선형미분방정식 해법을 시도하십시오.")
                else:
                    pass  # x항이 우변에 잘 있으므로 따로 옮기지 않는다.
            elif 'y' in term_data[1][i]:
                if 'x' in term_data[1][i] and 'exp' not in term_data[1][i]:  # x만 위치 감지하면 exp도 감지해 버려서 예외처리
                    print("선형미분방정식 해법을 시도하십시오.")
                else:  # y항이 우변에 있으므로 양변에 나누기 (y항)
                    term_data[0].append('1/' + '(' + term_data[1][i] + ')')
                    del term_data[1][i]
        except IndexError:
            pass
    
    # term_data[0]이나 term_data[1]에 항이 여러 개 있을 경우, 그 항들 통합
    temp_eqstring = '1'
    if len(term_data[0]) == 1:
        term_data[0] = term_data[0][0]  # 쓸데없이 있는 [] 없애기
    elif len(term_data[0]) > 1:  # 항 통합 필요
        for i in range(len(term_data[0])):
            temp_eqstring += '*(' + term_data[0][i] + ')'
        term_data[0] = temp_eqstring
    if term_data[0] == []:  # dy/dx 계수가 없을 경우는 1로 지정(1은 곱셈의 항등원)
        #print("프로그램 상에서 dy/dx의 계수가 할당되지 않았습니다. 곱셈의 항등원인 1로 할당합니다.")
        term_data[0] = '1'

    temp_eqstring = '1'
    if len(term_data[1]) == 1:
        term_data[1] = term_data[1][0]
    elif len(term_data[1]) > 1:  # 항 통합 필요
        for i in range(len(term_data[1])):
            temp_eqstring += '*(' + term_data[1][i] + ')'
        term_data[1] = temp_eqstring

    term_data[0] = factor(term_data[0])
    term_data[1] = factor(term_data[1])

    term_data[0] = str(factor(integrate(term_data[0], y)))
    term_data[1] = str(factor(integrate(term_data[1], x)))

    try:
        term_data[0] = term_data[0].replace("exp(1.0*I*pi)", "-1")  # 오일러 공식. 수학에서 가장 아름답다는 그 공식. 근데 sympy에서는 인식 못 함.
        term_data[1] = term_data[1].replace("exp(1.0*I*pi)", "-1")
        term_data[0] = str(factor(term_data[0]))
        term_data[1] = str(factor(term_data[1]))
        term_data[0] = term_data[0].replace('exp','e^') #지수 부분의 exp나 **를 ^로 치환.
        term_data[0] = term_data[0].replace('**','^')
        term_data[0] = term_data[0].replace(' ','')
        term_data[1] = term_data[1].replace('exp','e^')
        term_data[1] = term_data[1].replace('**','^')
        term_data[1] = term_data[1].replace(' ','')
    except:
        pass
    # print(term_data)
    return term_data  # [좌변 y 적분값, 우변 x 적분값] list 반환



# 되는 애!
print(divide_val_derivative("(yp)=((1)+(x)+(y)+(x*y))*((x)+(1))"))
# 되는 애!
print(divide_val_derivative("(exp(x))=(yp)"))
# 되는 애!
# divide_val_derivative("((exp(x))^2)=(yp)")
print(divide_val_derivative("((exp(x))**2)=(yp)"))
# 되는 애!
print(divide_val_derivative("(x**0.5)*(yp)=exp((y)+(x**0.5))"))
# 되는 애!
print(divide_val_derivative('(yp)=(y)*sin(x)'))
# 되는 애!
print(divide_val_derivative("(x**0.5)(yp)=exp(y+x**0.5)"))
# 되는 애!
print(divide_val_derivative("(yp)=(exp(x))"))
# 안 되는 애! (이유: yp에 괄호 안 씌움.)
# print(divide_val_derivative("((exp(x))*yp)=((exp(x))**0.5)"))