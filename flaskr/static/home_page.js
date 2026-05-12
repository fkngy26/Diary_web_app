// local easy DB
let Tasks=[];

const apiHogeUrl="http://127.0.0.1:5000/api/hoge"
const apiDBUrl="http://127.0.0.1:5000/api/inputDB"

const initialize=()=>{
    // サーバからのデータの受け取り
    fetch(apiHogeUrl)
    .then((response)=>response.json())
    .then((data)=>{
        console.log(data)
    })
    // サーバにデータの受け渡し
    fetch(apiDBUrl,{
        method:'POST',
        headers:{
            'Content-Type':'apilication/json'
        },
        body:JSON.stringify({
            'message':'data from front'
        })
    })
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

initialize();