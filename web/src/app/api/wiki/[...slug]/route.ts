import { NextResponse } from "next/server";
import { readMarkdownFile } from "@/lib/wiki";

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ slug: string[] }> }
) {
  const { slug } = await params;
  const filePath = `wiki/${slug.join("/")}.md`;
  const content = readMarkdownFile(filePath);

  if (!content) {
    return NextResponse.json(
      { error: "Article not found" },
      { status: 404 }
    );
  }

  return NextResponse.json({ content, slug: slug.join("/") });
}
