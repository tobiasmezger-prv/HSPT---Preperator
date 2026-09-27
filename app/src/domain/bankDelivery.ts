import {validateManifest,validateBank} from './contentSchema.mjs';
import {loadBank,installBank,type InstalledBank} from './storage';
export async function sha256(text:string){const bytes=new TextEncoder().encode(text);return [...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(x=>x.toString(16).padStart(2,'0')).join('');}
let pending:Promise<InstalledBank>|undefined;
export function checkForBank(fetcher:typeof fetch=fetch){
 if(pending)return pending;
 pending=(async()=>{
  const signal=AbortSignal.timeout(15000);
  const response=await fetcher('/content/manifest.json',{cache:'no-store',signal});if(!response.ok)throw new Error('Question update unavailable.');const manifest=validateManifest(await response.json());
  let installed=await loadBank().catch(()=>null);if(installed){try{validateBank(installed.bank,installed.manifest);}catch{installed=null;}}if(installed?.manifest.releaseId===manifest.releaseId&&installed.manifest.checksum===manifest.checksum)return installed;
  const content=await fetcher(manifest.bankUrl,{cache:'no-cache',signal});if(!content.ok)throw new Error('Question download failed.');const text=await content.text();if(text.length>20_000_000)throw new Error('Question file is too large.');if(await sha256(text)!==manifest.checksum)throw new Error('Question checksum failed.');const bank=validateBank(JSON.parse(text),manifest);const value={bank,manifest};try{await installBank(value);}catch{throw Object.assign(new Error('Questions downloaded, but this browser could not save them.'),{downloadedBank:value});}return value;
 })().finally(()=>{pending=undefined;});return pending;
}
