import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
const ACCOUNT = process.env.R2_ACCOUNT_ID;
const KEY = process.env.R2_ACCESS_KEY_ID;
const SECRET = process.env.R2_SECRET_ACCESS_KEY;
const BUCKET = process.env.R2_BUCKET;
const PUBLIC_BASE = process.env.R2_PUBLIC_BASE;
export function storageConfigured() { return !!(ACCOUNT && KEY && SECRET && BUCKET); }
export async function presignPut(name: string, type: string) {
  if (!storageConfigured()) throw new Error("storage not configured");
  const client = new S3Client({ region: "auto", endpoint: `https://${ACCOUNT}.r2.cloudflarestorage.com`, credentials: { accessKeyId: KEY as string, secretAccessKey: SECRET as string } });
  const safe = name.replace(/[^a-zA-Z0-9._-]/g, "_");
  const objectKey = `uploads/${Date.now()}-${Math.random().toString(36).slice(2, 8)}-${safe}`;
  const cmd = new PutObjectCommand({ Bucket: BUCKET as string, Key: objectKey, ContentType: type || "application/octet-stream" });
  const uploadUrl = await getSignedUrl(client, cmd, { expiresIn: 3600 });
  const publicUrl = PUBLIC_BASE ? `${PUBLIC_BASE.replace(/\/$/, "")}/${objectKey}` : null;
  return { uploadUrl, key: objectKey, publicUrl };
}
