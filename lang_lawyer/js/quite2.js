function quote(s) { return String.fromCharCode(96) + s + String.fromCharCode(96) };
var s=`function quote(s) { return String.fromCharCode(96) + s + String.fromCharCode(96) };
var s=X;
console.log(s.replace("X", quote(s)));`;
console.log(s.replace("X", quote(s)));
