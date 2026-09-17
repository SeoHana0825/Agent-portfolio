## 📝 Java 컬렉션 퀴즈

### 문제
다음 코드를 보고 물음에 답하세요:

```java
import java.util.*;

public class CollectionTest {
    public static void main(String[] args) {
        // (A) 중복을 허용하지 않는 컬렉션 생성
        ______<String> fruits = new ______<>();
        
        fruits.add("사과");
        fruits.add("바나나");
        fruits.add("사과");  // 중복 추가
        fruits.add("오렌지");
        
        System.out.println(fruits.size());  // 출력값은?
    }
}
```

**질문:** 
1. 빈칸 (A) 에 들어갈 적절한 컬렉션 클래스는 무엇인가요?
2. `fruits.size()` 의 출력값은 얼마인가요?

---

### [힌트 1 단계] 🔑
**키워드:** 중복 불가, Set 인터페이스

---

### [힌트 2 단계] 💡
**예시 코드:**
```java
import java.util.*;

public class Example {
    public static void main(String[] args) {
        // 중복을 허용하지 않는 컬렉션
        ______<Integer> numbers = new ______<>();
        
        numbers.add(1);
        numbers.add(2);
        numbers.add(1);  // 중복
        
        System.out.println(numbers.size());  // ?
    }
}
```

---

### [힌트 3 단계] 📋
**유사 코드 완성본:**
```java
import java.util.*;

public class StudentSet {
    public static void main(String[] args) {
        // 학생 ID 를 저장하는 중복 불가 컬렉션
        HashSet<String> studentIds = new HashSet<>();
        
        studentIds.add("2024001");
        studentIds.add("2024002");
        studentIds.add("2024001");  // 중복 ID 추가
        
        System.out.println(studentIds.size());  // 2 출력
    }
}
```

---

### [정답] ✅
```java
import java.util.*;

public class CollectionTest {
    public static void main(String[] args) {
        /**
         * HashSet: 해시 테이블 기반의 Set 구현체
         * - 중복을 허용하지 않음 (중복 add() 는 무시됨)
         * - 순서를 보장하지 않음
         * - null 값을 하나의 요소로 허용
         */
        HashSet<String> fruits = new HashSet<>();
        // 또는: Set<String> fruits = new HashSet<>(); (인터페이스로 선언 - 권장)
        
        fruits.add("사과");      // 추가됨
        fruits.add("바나나");    // 추가됨
        fruits.add("사과");      // 중복이므로 무시됨
        fruits.add("오렌지");    // 추가됨
        
        // 실제 저장된 요소: 사과, 바나나, 오렌지 (총 3 개)
        System.out.println(fruits.size());  // 출력: 3
    }
}
```

**정답:** 
1. **HashSet** (또는 Set)
2. **3**

---

### 📚 핵심 개념 정리
- **ArrayList**: 순서 보장, 중복 허용, 인덱스 접근 O
- **HashSet**: 순서 보장 X, 중복 불가, 해시 기반
- **HashMap**: 키 - 값 쌍 저장, 키는 중복 불가
