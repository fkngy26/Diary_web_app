// local easy DB
let Tasks=[];

const initialize=()=>{
    console.log("init");
}

let addTaskButton=document.getElementById("addTaskBtn");
addTaskButton.addEventListener("click",()=>{
    // 記入欄のポップが出る
    let task=prompt("タスクを追加")
    // OKを押すとタスクがTasksに追加
    Tasks.push(task);
    let toDoList=document.getElementById("iToDoList");
    addTaskView(Tasks[Tasks.length-1],toDoList);
});

let saveTodayData=document.getElementById("saveTodayData");
saveTodayData.addEventListener("click",()=>{
    // オブジェクトを取ってくる
    let toDoList=document.getElementsByClassName("task");
    let todayDiary=document.getElementById("Diary");
    // DBに対応する形で保存する
    console.log(toDoList)
    let count=0;
    for(let i=0;i<Tasks.length;i++){
        if(toDoList[i].checked===true){
            count++;
        }
    }
    alert(count);
})

const addTaskView=(taskName,listObj)=>{
    // ラベルのオブジェクトを作成
    let label=document.createElement("label");

    // チェックボックスオブジェクトを作成
    let checkbox=document.createElement("input");
    checkbox.type="checkbox";
    checkbox.classList.add("task");

    // タスク表示オブジェクトを作成
    let text=document.createElement("span");
    text.textContent=taskName;

    // それぞれを合体させる
    label.appendChild(checkbox);
    label.appendChild(text);
    label.classList.add("taskObj");

    // リストオブジェクトにくっつける
    // let toDoList=document.getElementById("iToDoList");
    listObj.appendChild(label);
}

const sent=()=>{
    fetch(["http://127.0.0.1:5000"]) // リクエストを送信
	.then((response) => response.json())
	.then((data) => {console.log(data);});

    console.log(text)
}

initialize();
sent();