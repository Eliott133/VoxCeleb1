function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs < 10 ? "0" : ""}${secs}`;
}

function formatDateTime(date){
    return (date.getDate()+"_"+date.getMonth()+"_"+date.getFullYear()+"_"+date.getHours()+":"+date.getMinutes()+":"+date.getSeconds());
}

