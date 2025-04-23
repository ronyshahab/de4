import { callApi } from "./utils.js";

const uploadImage = async(e) => {
  e.preventDefault();
    const input = document.getElementById('imageInput');
    const file = input.files[0];

    if (!file) {
      alert("Please select an image.");
      return;
    }

    const formData = new FormData();
    formData.append("image", file);

    const response = await callApi("POST", "/upload", {body:formData});
    console.log(response)
}

const startVer = async (e) =>{
  e.preventDefault();
  const response = await callApi("GET", "/start",);
  console.log(response);
}

const stopVer = async (e) =>{
  e.preventDefault();
  const response = await callApi("GET", "/stop",);
  console.log(response);
}


window.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("uploadForm");
  const startBtn = document.getElementById("startBtn");
  const stopBtn = document.getElementById("stopBtn");

  form.addEventListener("submit", uploadImage);
  startBtn.addEventListener("click", startVer);
  stopBtn.addEventListener("click", stopVer);
});
