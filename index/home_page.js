let Tasks=["Get up","sleep","study"];

const initialize=()=>{    
    for(let i=0;i<Tasks.length;i++){
        addTask(i);
    }
}
// setAttributeを使用して、繰り返しながらもidを一意に定めることができるらしい
// これにより、label.forが機能するようになる。
// CSSでは改行をするのではなく、inline設定からblock設定で横並びから縦並びにすることができる。
// ToDoの中のlabelにだけ、CSSを適用したいといった2つ以上の条件を適用したい差異は、CSSセレクタと呼ばれるものを理解する必要があるらしい。
const addTask=(task_num)=>{
    let task_list=document.getElementById("iToDoList");
    let label=document.createElement("label");
    label.for="task"
    let checkbox=document.createElement("input");
    checkbox.type="checkbox";
    checkbox.id="task";
    let text=document.createElement("span");
    text.textContent=Tasks[task_num];

    label.appendChild(checkbox);
    label.appendChild(text);

    task_list.appendChild(label);
}

initialize();