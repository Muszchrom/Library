import React, { useEffect, useRef, useState } from "react";
import { Input } from "./ui/input";

export default function ImageInput() {
  const inputRef = useRef<HTMLInputElement>(null);
  const dropdownBox = useRef<HTMLDivElement>(null);
  const [draggedOver, setDraggedOver] = useState(false);
  const [imageUrl, setImageUrl] = useState("");

  const [userImage, setUserImage] = useState<File>();

  useEffect(() => {
    if (!userImage) return
    displayImage(userImage)
    setDraggedOver(false)
  }, [userImage])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;
    setUserImage(e.target.files[0]);
  }

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (!e.dataTransfer.files) return;
    setUserImage(e.dataTransfer.files[0]);
  }

  const displayImage = (file: File) => {
    const reader = new FileReader();
    reader.onload = (e: ProgressEvent<FileReader>) => {
      const f = e.target!.result as string
      setImageUrl(f)
    }
    reader.readAsDataURL(file);
  }

  return (
    <>
      <Input ref={inputRef} 
             onChange={handleChange} 
             type="file" 
             accept="image/*" 
             className="hidden"/>
      <div ref={dropdownBox}
           title="Drop image here"
           className="w-full aspect-video border flex items-center justify-center"
           onDrop={handleDrop}
           onDragOver={(e: React.DragEvent<HTMLDivElement>) => e.preventDefault()}
           onDragEnter={() => setDraggedOver(true)}
           onDragLeave={() => setDraggedOver(false)}
           onClick={() => inputRef.current!.click()}>
        {imageUrl.length ? (
          <img src={imageUrl} style={{filter: draggedOver ? "brightness(0.9)" : "brightness(1)"}}/>
        ) : (
          <svg className="stroke-foreground" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" pointerEvents={"none"}>
            <path d="M4 14V18H20V14M12 6L8 10M12 6L16 10M12 6V14" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        )}
      </div>
    </>
  );
}