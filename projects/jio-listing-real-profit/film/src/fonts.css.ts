import {staticFile} from 'remotion';
export const fontCss = `
@font-face{font-family:P;font-weight:700;src:url(${staticFile('poppins-latin-700-normal.woff2')}) format('woff2')}
@font-face{font-family:P;font-weight:800;src:url(${staticFile('poppins-latin-800-normal.woff2')}) format('woff2')}
@font-face{font-family:P;font-weight:800;unicode-range:U+0900-097F,U+20B9;src:url(${staticFile('poppins-devanagari-800-normal.woff2')}) format('woff2')}
@font-face{font-family:P;font-weight:500;src:url(${staticFile('poppins-latin-500-normal.woff2')}) format('woff2')}`;
