import type {Question} from './types';
export type Manifest={releaseId:string;schemaVersion:1;publishedAt:string;bankUrl:string;questionCount:number;checksum:string};
export type Bank={releaseId:string;schemaVersion:1;questions:Question[]};
export const schemaVersion:number;
export function validateQuestion(q:unknown,published?:boolean):Question;
export function validateManifest(m:unknown):Manifest;
export function validateBank(b:unknown,m:Manifest):Bank;
