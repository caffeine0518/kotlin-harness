---
severity: error
applies_to: "**/*.kt"
source: https://developer.android.com/topic/libraries/view-binding#fragments
---

# 프래그먼트 필드에 보관한 뷰 바인딩은 `onDestroyView()` 에서 `null` 로 해제한다

## 이유

프래그먼트는 자신의 뷰보다 오래 유지된다(백 스택에 있는 경우 등). 공식 문서는 바인딩 클래스 인스턴스에 대한 참조를 `onDestroyView()` 에서 해제하라고 한다. 해제하지 않으면 바인딩이 파괴된 뷰 계층 전체를 참조해 메모리 누수가 된다.

## 위반

```kotlin
class ProfileFragment : Fragment() {
    private lateinit var binding: ResultProfileBinding  // null 로 해제할 수 없다

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        binding = ResultProfileBinding.inflate(inflater, container, false)
        return binding.root
    }
}

class SettingsFragment : Fragment() {
    private var _binding: FragmentSettingsBinding? = null
    // onDestroyView() 를 오버라이드하지 않았거나, 오버라이드했지만 _binding = null 이 없다
}
```

## 수정

```kotlin
class ProfileFragment : Fragment() {
    private var _binding: ResultProfileBinding? = null
    // onCreateView 와 onDestroyView 사이에서만 유효하다
    private val binding get() = _binding!!

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        _binding = ResultProfileBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
```

## 허용

- `onViewCreated` 에서 `val binding = FragmentXBinding.bind(view)` 처럼 로컬 변수로만 쓰는 경우
- 뷰 생명주기(`viewLifecycleOwner`)에 맞춰 값을 자동으로 해제하는 프로퍼티 델리게이트로 보관하는 경우
- 액티비티의 바인딩 필드. 액티비티는 뷰와 수명이 같다.
- 위 수정 예시의 `_binding!!` 게터는 공식 문서의 패턴이므로 `common/null-safety/not-null-assertion` 으로 보고하지 않는다.
