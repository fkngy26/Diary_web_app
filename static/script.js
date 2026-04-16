const btn = document.getElementById("btn");
const list = document.getElementById("list");

// 追加
btn.addEventListener("click", async () => {
    const input = document.getElementById("todoInput");
    if (!input.value) return;

    await fetch("/todos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: input.value })
    });

    input.value = "";
    loadTodos();
});

// 取得して表示
async function loadTodos() {
    const res = await fetch("/todos");
    const todos = await res.json();

    list.innerHTML = "";

    todos.forEach(todo => {
        const li = document.createElement("li");
        li.textContent = todo.text;
        list.appendChild(li);
    });
}

// 初期表示
loadTodos();