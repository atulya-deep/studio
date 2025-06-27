import * as React from "react";

export function Logo() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 100 100"
      className="h-8 w-8"
    >
      <circle cx="50" cy="50" r="50" fill="black" />
      <path
        d="M90,65 A40,40 0 0 1 35,90"
        stroke="#ca8a04"
        strokeWidth="5"
        fill="none"
      />
      <path
        d="M10,35 A40,40 0 0 1 65,10"
        stroke="#ca8a04"
        strokeWidth="5"
        fill="none"
      />
      <text
        x="50"
        y="62"
        fontFamily="sans-serif"
        fontSize="40"
        fontWeight="bold"
        fill="white"
        textAnchor="middle"
      >
        OFI
      </text>
      <circle cx="73" cy="32" r="5" fill="#ca8a04" />
    </svg>
  );
}
