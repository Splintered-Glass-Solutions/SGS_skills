"use client";

export function PrintButton() {
  return (
    <button className="cover-print-button" type="button" onClick={() => window.print()}>
      Download PDF
    </button>
  );
}
