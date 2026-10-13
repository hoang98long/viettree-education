"use client";

import Image from "next/image";
import { useId } from "react";
import {
  fractionPicture,
  pictureWords,
  placeValuePicture,
  smallSum,
} from "@/lib/guided-reading";

export function BlockPictures({ text }: { text: string }) {
  const pictures = pictureWords(text);
  const sum = smallSum(text);
  const fraction = fractionPicture(text);
  const placeValues = placeValuePicture(text);
  const label = useId();
  if (!pictures.length && !sum && !fraction && !placeValues) return null;
  return (
    <div className="lesson-picture-strip" aria-label="Tranh giúp em hiểu bài">
      {pictures.map((picture) => (
        <figure key={picture.code} className="lesson-word-picture">
          <Image
            src={`/learning/${picture.code}.svg`}
            alt={picture.label}
            width={120}
            height={120}
          />
          <figcaption>{picture.label}</figcaption>
        </figure>
      ))}
      {sum && (
        <figure className="lesson-count-picture">
          <svg viewBox="0 0 400 130" role="img" aria-labelledby={label}>
            <title id={label}>
              {sum.a} chấm xanh cộng {sum.b} chấm vàng bằng {sum.a + sum.b} chấm
            </title>
            {Array.from({ length: sum.a + sum.b }, (_, i) => (
              <circle
                key={i}
                cx={20 + (i % 10) * 39}
                cy={30 + Math.floor(i / 10) * 40}
                r="12"
                fill={i < sum.a ? "#23805b" : "#e4a733"}
              />
            ))}
            <text
              x="200"
              y="119"
              textAnchor="middle"
              fontSize="24"
              fill="#203d34"
            >
              {sum.a} + {sum.b} = {sum.a + sum.b}
            </text>
          </svg>
          <figcaption>Đếm hai nhóm chấm để kiểm tra.</figcaption>
        </figure>
      )}
      {fraction && (
        <figure className="lesson-fraction-picture">
          <div
            role="img"
            aria-label={`${fraction.numerator} trên ${fraction.denominator} phần bằng nhau`}
            className="fraction-parts"
          >
            {Array.from({ length: fraction.denominator }, (_, i) => (
              <span
                key={i}
                className={i < fraction.numerator ? "filled" : ""}
              />
            ))}
          </div>
          <figcaption>
            {fraction.numerator}/{fraction.denominator} · Các phần bằng nhau
          </figcaption>
        </figure>
      )}
      {placeValues && (
        <dl className="lesson-place-value" aria-label="Tách các hàng của số">
          {placeValues.map((value, i) => (
            <div key={i}>
              <dt>{value.label}</dt>
              <dd>{value.digit}</dd>
            </div>
          ))}
        </dl>
      )}
    </div>
  );
}
