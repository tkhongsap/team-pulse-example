import Link from "next/link";
import { notFound } from "next/navigation";
import matter from "gray-matter";
import { readMarkdownFile } from "@/lib/wiki";
import { WikiMarkdownRenderer } from "@/components/wiki-markdown-renderer";
import { Badge } from "@/components/ui/badge";

interface WikiPageProps {
  params: Promise<{ slug: string[] }>;
}

export default async function WikiPage({ params }: WikiPageProps) {
  const { slug } = await params;
  const filePath = `wiki/${slug.join("/")}.md`;
  const rawContent = readMarkdownFile(filePath);

  if (!rawContent) {
    notFound();
  }

  const { data: frontmatter, content } = matter(rawContent);

  return (
    <div className="max-w-4xl mx-auto px-6 py-6">
      <div className="flex items-center gap-3 mb-4">
        <Link
          href="/"
          className="text-sm text-muted-foreground hover:text-foreground"
        >
          &larr; Back to Chat
        </Link>
        <span className="text-sm text-muted-foreground">|</span>
        <span className="text-sm text-muted-foreground">
          wiki/{slug.join("/")}
        </span>
      </div>

      {/* Frontmatter metadata header */}
      {frontmatter.title && (
        <div className="mb-6 pb-4 border-b border-border">
          <h1 className="text-2xl font-semibold">{frontmatter.title}</h1>
          <div className="flex flex-wrap items-center gap-2 mt-2">
            {frontmatter.tags?.map((tag: string) => (
              <Badge key={tag} variant="secondary">
                {tag}
              </Badge>
            ))}
            {frontmatter.updated && (
              <span className="text-xs text-muted-foreground">
                Updated: {frontmatter.updated}
              </span>
            )}
            {frontmatter.created && (
              <span className="text-xs text-muted-foreground">
                Created: {frontmatter.created}
              </span>
            )}
          </div>
        </div>
      )}

      <WikiMarkdownRenderer content={content} />
    </div>
  );
}
