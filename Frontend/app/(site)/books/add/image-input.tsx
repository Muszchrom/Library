import { useEffect, useRef, useState } from "react";
import { ControllerRenderProps, UseFormRegisterReturn } from "react-hook-form";
import { Input } from "@/components/ui/input";
import { FormControl, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { cn } from "@/lib/utils";

export default function ImageInput({ field, fileRef }: 
  { field: ControllerRenderProps<{
      author: number;
      isbn: string;
      isbn13: string;
      title: string;
      description: string;
      publication_date: string;
      cover?: "";
    }, "cover">, 
    fileRef: UseFormRegisterReturn<"cover">}) {

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
    field.onChange(e.target?.files ?? undefined)
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
    <FormItem>
      <FormLabel>Zdjęcie okładki</FormLabel>
      <FormControl>
        <>
          <Input
            { ...fileRef }
            ref={inputRef} 
            onChange={handleChange} 
            type="file" 
            accept="image/*" 
            className="hidden "/>
          <div 
            ref={dropdownBox}
            title="Drop image here"
            className="w-full aspect-video border flex items-center justify-center rounded-md overflow-hidden relative"
            onDrop={handleDrop}
            onDragOver={(e: React.DragEvent<HTMLDivElement>) => e.preventDefault()}
            onDragEnter={() => setDraggedOver(true)}
            onDragLeave={() => setDraggedOver(false)}
            onClick={() => inputRef.current!.click()}>

            {imageUrl.length ? (
              <div className={cn("w-full h-full relative")}>
                <picture>
                  <img src={imageUrl} alt="Przesłane zdjęcie okładki" className={cn("w-full h-full object-contain relative z-10", draggedOver && "brightness-75")} />
                </picture>
                <picture>
                  <img src={imageUrl} alt="" className={cn("w-full h-full object-cover absolute top-0 blur-md", draggedOver && "brightness-75")} />
                </picture>
                <div className={cn("pointer-events-none absolute top-0 bottom-0 left-0 right-0 items-center justify-center z-10", draggedOver ? "flex" : "hidden")}>
                  <svg className="stroke-foreground bounce-reverse" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" pointerEvents={"none"}>
                    <path d="M4 14V18H20V14M12 6L8 10M12 6L16 10M12 6V14" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </div>
              </div>
            ) : (
              <div className="absolute top-0 bottom-0 left-0 right-0 flex items-center justify-center z-10">
                <svg className={cn("stroke-foreground", draggedOver && "bounce-reverse")} width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" pointerEvents={"none"}>
                  <path d="M4 14V18H20V14M12 6L8 10M12 6L16 10M12 6V14" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
            )}
            
            {/* <div className="absolute top-0 bottom-0 left-0 right-0 flex items-center justify-center z-10">
              <svg className="stroke-foreground animate-bounce" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" pointerEvents={"none"}>
                <path d="M4 14V18H20V14M12 6L8 10M12 6L16 10M12 6V14" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div> */}
          </div>
        </>
      </FormControl>
      <FormMessage />
    </FormItem>
  );
}