import { defineConfig } from 'astro/config';
export default defineConfig({
  site: 'https://datapoints.semanticmachines.fyi',
  output: 'static',
  outDir: './site',
  publicDir: './.generated/public',
  trailingSlash: 'always',
  compressHTML: false,
});
