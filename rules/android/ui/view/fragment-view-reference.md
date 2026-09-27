---
severity: error
applies_to: "**/*.kt"
source: https://developer.android.com/guide/fragments/lifecycle#fragment_created_and_view_destroyed
---

# 프래그먼트 필드에 보관한 `View` 참조는 `onDestroyView()` 에서 해제한다

## 이유

프래그먼트의 뷰는 프래그먼트와 별도의 생명주기를 가진다. `onDestroyView()` 가 호출되면 뷰의 생명주기가 끝나고, 공식 문서는 이 시점에 프래그먼트의 뷰에 대한 모든 참조를 제거해 가비지 컬렉션될 수 있게 하라고 한다. 프래그먼트가 백 스택에 남아 있는 동안 필드가 파괴된 뷰를 계속 참조하면 메모리 누수가 된다. `View` 를 참조하는 어댑터·리스너·헬퍼 객체도 같다.

## 위반

```kotlin
class ListFragment : Fragment() {
    private lateinit var recyclerView: RecyclerView
    private var titleView: TextView? = null  // onDestroyView 에서 null 로 해제하지 않는다

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        recyclerView = view.findViewById(R.id.list)
        titleView = view.findViewById(R.id.title)
    }
}
```

## 수정

뷰가 필요한 곳에서 로컬 변수로 받거나, 널러블 필드로 보관하고 `onDestroyView()` 에서 `null` 로 해제한다.

```kotlin
class ListFragment : Fragment() {
    private var titleView: TextView? = null

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        val recyclerView = view.findViewById<RecyclerView>(R.id.list)
        recyclerView.adapter = adapter
        titleView = view.findViewById(R.id.title)
    }

    override fun onDestroyView() {
        super.onDestroyView()
        titleView = null
    }
}
```

## 허용

- 액티비티·커스텀 `View` 의 `View` 필드
- `View` 를 참조하지 않는 필드(데이터만 가진 어댑터 등)
- 뷰 바인딩 필드는 `android/ui/view/fragment-binding-cleanup` 으로 보고한다.
