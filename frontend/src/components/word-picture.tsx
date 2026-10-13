import Image from "next/image";
import { pictureForLabel } from "@/lib/learning-pictures";

export function WordPicture({ text }: { text: string }) {
  const picture = pictureForLabel(text);
  if (!picture) return null;
  return (
    <Image
      className="word-picture"
      src={`/learning/${picture.code}.svg`}
      alt=""
      aria-hidden="true"
      width={80}
      height={80}
      draggable={false}
    />
  );
}
