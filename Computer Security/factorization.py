import threading
import time
from math import sqrt, gcd, floor, exp, log
import numpy as np
from functools import reduce
import math
import random


def isPrime(n, k=5):  # miller-rabin
    from random import randint
    if n < 2: return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        if n % p == 0: return n == p
    s, d = 0, n - 1
    while d % 2 == 0:
        s, d = s + 1, d // 2
    for i in range(k):
        x = pow(randint(2, n - 1), d, n)
        if x == 1 or x == n - 1: continue
        for r in range(1, s):
            x = (x * x) % n
            if x == 1: return False
            if x == n - 1: break
        else:
            return False
    return True


def bitlength(x):
    assert x >= 0
    n = 0
    while x > 0:
        n = n + 1
        x = x >> 1
    return n


def isqrt(n):
    if n < 0:
        raise ValueError('square root not defined for negative numbers')

    if n == 0:
        return 0
    a, b = divmod(bitlength(n), 2)
    x = 2 ** (a + b)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y


def is_perfect_square(n):
    h = n & 0xF;  # last hexadecimal "digit"
    if h > 9:
        return -1  # return immediately in 6 cases out of 16.
    # Take advantage of Boolean short-circuit evaluation
    if (h != 2 and h != 3 and h != 5 and h != 6 and h != 7 and h != 8):
        # take square root if you must
        t = isqrt(n)
        if t * t == n:
            return t
        else:
            return -1
    return -1


def timer(toc, tic, counter):
    if toc - tic > counter:
        print(f"Time: {toc - tic:0.4f} seconds")
        counter = counter + 5
    return counter


def dixon_factor_f(n, max_time):
    global toc

    def _initialize_bound(nm):
        # https://github.com/brendongo/factoring/blob/master/dixons.py
        return int(floor(exp(sqrt(log(nm) * log(log(nm))) / 2)))

    def factors_f(b):
        # https://stackoverflow.com/questions/6800193/what-is-the-most-efficient-way-of-finding-all-the-factors-of-a-number-in-python
        step = 2 if n % 2 else 1
        return reduce(list.__add__,
                      ([i, b // i] for i in range(1, int(sqrt(b)) + 1, step) if b % i == 0))

    print('Starting Dixon algorithm for ', n)
    tic = time.perf_counter()
    counter = 0
    bound = _initialize_bound(n)
    print('Bound found:', bound)
    factors = [2, 3, 5, 7]
    print('Factors found : ', factors)

    # start_n = int(sqrt(n))
    start_n = 0
    b_square_smooth_pairs = []
    for i in range(start_n, n):

        # timers
        toc = time.perf_counter()
        counter = timer(toc, tic, counter)
        if counter > max_time:
            raise Exception('No solution find on the given time')

        for j in range(len(factors)):
            lhs = pow(i, 2, n)
            rhs = pow(factors[j], 2, n)
            if lhs == rhs:
                b_square_smooth_pairs.append([i, factors[j]])
    # print('B squares found: ', b_square_smooth_pairs)

    arr = []
    for i in range(len(b_square_smooth_pairs)):

        toc = time.perf_counter()
        counter = timer(toc, tic, counter)
        if counter > max_time:
            raise Exception('Not solution find on the given time')

        factor = gcd(b_square_smooth_pairs[i][0] - b_square_smooth_pairs[i][1], n)
        if factor != 1:
            arr.append(factor)

    x = np.array(arr)
    print('Finished Dixon Algorithm on ', f"Time: {toc - tic:0.4f} seconds")
    return np.unique(x)


def pollard_f(n, bound, max_time):
    def primes(n):
        ps = []
        sieve = [True] * n
        for p in range(2, n):
            if sieve[p]:
                ps.append(p)
                for i in range(p * p, n, p):
                    sieve[i] = False
        return ps

    print('Starting Polland algorithm for ', n)
    tic = time.perf_counter()
    counter = 0

    c = 2
    for p in primes(bound):

        toc = time.perf_counter()
        counter = timer(toc, tic, counter)
        if counter > max_time:
            raise Exception('Not solution find on the given time')

        pp = p
        while pp < bound:
            c = pow(c, p, n)
            pp = pp * p
    g = gcd(c - 1, n)
    if 1 < g < n:
        return g, n // g
    raise Exception('Error factorising, try another bound ?')


def pollard_f_2(n):
    def pollard(n):
        a = 2
        i = 2
        while True:
            a = (a ** i) % n
            d = math.gcd((a - 1), n)
            if d > 1:
                return d
                break
            i += 1

    return pollard(n)


def weiner_attack_f(e, n, max_time):
    def get_continued_fract(x, y):
        a = x // y
        result = [a]
        while a * y != x:
            x, y = y, x - a * y
            a = x // y
            result.append(a)
        return result

    def convergents_from_continued_frac(continued_frac):
        convs = [];
        for i in range(len(continued_frac)):
            convs.append(contfrac_to_rational(continued_frac[0:i]))
        return convs

    def contfrac_to_rational(frac):
        if len(frac) == 0:
            return 0, 1
        num = frac[-1]
        denom = 1
        for _ in range(-2, -len(frac) - 1, -1):
            num, denom = frac[_] * num + denom, num
        return num, denom

    tic = time.perf_counter()
    counter = 0

    frac = get_continued_fract(e, n)
    convergents = convergents_from_continued_frac(frac)
    for (k, d) in convergents:

        toc = time.perf_counter()
        counter = timer(toc, tic, counter)
        if counter > max_time:
            raise Exception('No solution find on the given time')

        if k != 0 and (e * d - 1) % k == 0:
            phi = (e * d - 1) // k
            s = n - phi + 1
            discr = s * s - 4 * n
            if discr >= 0:
                t = is_perfect_square(discr)
                if t != -1 and (s + t) % 2 == 0:
                    print('Finished Weiner Algorithm on ', f"Time: {toc - tic:0.4f} seconds")
                    return d
    return 0


def try_factorising_with_d_2(e, d, n):
    # https://crypto.stackexchange.com/questions/13113/how-can-i-find-the-prime-numbers-used-in-rsa
    for g in range(1, 9):
        p = gcd(n, pow(g, ((d * e - 1) // 2 ** 2), n) - 1)
        q = n // p
        if isPrime(p, 20):
            print('p is', p)
            print('q is ', q)
            print(p * q == n)
            break


def try_factorising_with_d(e, d, n):
    k = d * e - 1
    found = False
    p = 0
    q = 0
    while not found:
        g = random.randint(1, n)
        t = k
        if t % 2 == 0:
            t = t // 2
            x = pow(g, t, n)
            y = gcd(x - 1, n)
            if x > 1 and y > 1:
                p = y
                q = n / y
                found = True
    return p, q


def try_factorising(n, time_secs, pollard_bound, bound_increase, pollard_times):
    try:
        dixon_result = dixon_factor_f(n, time_secs)
        print('Dixon factors are', dixon_result)
    except Exception as e:
        print('Exception happened : ' + str(e))

    print('========================\n========================')
    bound = pollard_bound
    for i in range(0, pollard_times):
        print('Trying POLLARD with bound: ', bound)
        try:
            pollard_result = pollard_f(n, bound, time_secs)
            print('Pollard factors are', pollard_result)
            print('N is ', n, '\nR is ', pollard_result[0] * pollard_result[1])
        except Exception as e:
            print('Exception happened : ' + str(e))
        bound = bound + bound_increase


if __name__ == "__main__":

    task1 = False
    task2 = False
    task3 = False
    task4 = True

    # Task1
    if task1:
        e_1 = 13093328595385160044165980293174831781402910433996829686049849079194139027017437963020433409654254598967784284273088466083085543342666840110989310331142491498938291460305295086828226541498060829091531200764423401195922683471453468703721689465669372303425266741388904901165666303328872760703619023190687995422691546642616899901532563750227860076575848959768161075100460255012577625565123868435724583614883870330213257657190685096528432418456665538846807560061020585626974490286664652793908833669424000276680931369139404546215686214432257377137376327944301552319505561125394344205596939320029134879444106807878438488137
        n_1 = 21986209349522598669810906865768024040510874833876982838576681331542309207547008218894072567095416373659497230133396569323359898371317789548133481802145312769895831863123149387038220821712773786960781756311664121510622866921173866500595409454901147010013471749478924826426822441873737331716495921635931883569963555187083485598206980529116827877795567026250074202265927360532074462873436662506582235080339443933241625359591476428997279199451820908821582619548286654231931531356251085596993523325271292315727665008270293782837742921563562663832006966733277787971278021005846570498685386487009374677868911522765753502223
        d_1 = weiner_attack_f(e_1, n_1, 10)
        print('d found :', d_1)
        if d_1 > 1:
            try_factorising_with_d_2(e_1, d_1, n_1)

    ## p is 170803660617699844386851179371474599914120074391670623284230456231340632216235823594317544657111290128163195498458345559009440054300896480626166775773958533737983722600643663176159640550714443040373686666386121518654700746808579670287028757522251425593880869139343315951714659486171542531688632207952963104791
    ## q is  128722120298891516680849108211505059970684911348260528052479414328384022122957801434486189807460443685722058827513709747673889238930116914135307935650318831517748716912179316086829620881991741566746407258036285814770215812039169913160740933036972568174490227113227591761773123921996685177815391205082415921353

    # Task2

    if task2:
        n_2 = 24430436836352483797063096106414774550335403158860524990373856944254297586018983298705492233654830523199692736514219239319146510300625339876324647894404893431924815784960576423322270642064447439532880084271906506181596791330255472317736274838975886982878636272375371266076163692482358755032762905350584467818322896256697824686362875462689754439034305568485764372282041358336076968265549938271297558180529807346415680592340188076635410423523198461463168140415659131710799290510682225326203262832075315314659506065014839527357257670962979561415126272979988642044180466409976304796211964778255235614585976098809592350027
        e_2 = 65537
        # p = print(pollard_f_2(n_2))
        p = 201802338323822247762976091312398953585365203464182021987954259021442074856059725386336671167057110186239586246391430373219782265224062444199720355929977151162091729083826303862872370046603937645608706305315346136611803579780695403143292373193235079862482776555201550917056154776371200000000000000000000000001
        q = n_2 // p
        print(n_2 == p * q)

        #p=201802338323822247762976091312398953585365203464182021987954259021442074856059725386336671167057110186239586246391430373219782265224062444199720355929977151162091729083826303862872370046603937645608706305315346136611803579780695403143292373193235079862482776555201550917056154776371200000000000000000000000001
        #q=121061217819736895841873936884083089330870560881680370467822468395190538367714840920450445114510967689554869749779971895880113238102014149285468820060945341075560185498026002399515443707709686559585850444389100313511190304311929000630644099804294564031108902176528627092011505496232835614585976098809592350027

    # Task 3
    if task3:
        e_3 = 4540739216185503944360317693727598425914265679950045193021325112310705634291619065008907799345804742158053789146296680446894494207857215362393461454740251861270045084357114733204905034770917891701793191139362007652012678514584941575186023625310517580446149923208688962903396756745069246710893893015854244396440602337384016923965920177062914455924380937065037932267969029224822211730100507762697227846127311177385930201779337513938673664269014723153905166514932029992336846458567909977502925990713226059794678425101890459773253915812357018757128150035920553537530136211737469309110690361713502937223534374706564266353
        n_3 = 11504527348504158734037780170377498878712004214260381608730500717991815279122806648544220211648205780154761466805683032692581326833774139612636039191040833561873869035670800926010549835734364594410395476885067722861580093389878040520372281552748236896416214306849077757975842715196976800713818245047806206651294270657799988276627708411462924090113406327688546733972246647011570643506334873954567135880261896080553702646403928357768206828842771519038916167325592923329250827223365152756794305129647653055443711932408387687334586308353275284499524570044721152926963826516772537698976072032292400126788019940915306214671
        d_3 = weiner_attack_f(e_3, n_3, 10)
        print('d found :', d_3)
        if d_3 > 0:
            try_factorising_with_d_2(e_3, d_3, n_3)

    # p is 95122153533143958793575101382023276292294088612808646584559115629973211280738149214016120593922299186514612223346211491263572324852175448915457225508096896362901324234244231924977769204685214503684267913869526354710811942804195997771308503824094090937857949260676491972273802606178562579168486321151594762139
    # q is 120944773863804188714015975666717756816301519446824647999863115102065605973878912340045856162474408383121543730374527851500410213142615410104178185658269191089284023710242150649963959085226126429577122756017131077884270991667145752904575367675415498756316235742886894465243502530825987252280113337729269733789

    if task4:
        e_4 = 65537
        n_4 = 21991232899020757667180708939003545471279700034913931387275370649484106213493746354134516938874683722532376522428739266831139982942037647489613088565834625396270116948482205233937311403693804017272705867342159850843308530001872731667565741346582215077293242970006473486509965365929587251903494207313928176058515727281298368666934123057519040352255360265190524877179165787262999219352376695956654193963802488345737739750543388868502221204357840956405751039414535031641247236228671392078875980200356717694181270438688970492725419513292742560009022330977944092829578706789218989389932864305999884300269715051661053097943
        #print(pollard_f_2(n_4))
        p = 289808331960851737771759803525087737335855755367096019474685543005145912741210826243913523913735837567991589842550928695116960878879769477359746539719590978358151867193191260774291907964146799773722581429252590602423600156461241891433764242585143412511606610899753360453071807137080934400000000000000000000001
        q = n_4 // p
        print(n_4 == p * q)
        #p=289808331960851737771759803525087737335855755367096019474685543005145912741210826243913523913735837567991589842550928695116960878879769477359746539719590978358151867193191260774291907964146799773722581429252590602423600156461241891433764242585143412511606610899753360453071807137080934400000000000000000000001
        #q=75881989831787878698795302444385080712072005550233655066040851486716894141246390304315061621635456367692593343879429999810482859770450442899238266385213650364434396147195322667439244566369802803433781209508750613775711707572576311641175510832168423380380974519970597965509109264841945100269715051661053097943