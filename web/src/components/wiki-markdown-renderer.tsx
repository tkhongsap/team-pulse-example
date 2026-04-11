"use client";

import Link from "next/link";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface WikiMarkdownRendererProps {
  content: string;
}

function WikiLink({ slug }: { slug: string }) {
  const name = slug.split("/").pop() || slug;
  return (
    <Link
      href={`/wiki/${slug}`}
      className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-primary/10 text-primary border border-primary/20 hover:bg-primary/20 transition-colors"
    >
      {name}
    </Link>
  );
}

function processWikilinks(text: string): React.ReactNode[] {
  const parts = text.split(/(\[\[.+?\]\])/g);
  return parts.map((part, i) => {
    const match = part.match(/^\[\[(.+?)\]\]$/);
    if (match) {
      return <WikiLink key={i} slug={match[1]} />;
    }
    return part;
  });
}

export function WikiMarkdownRenderer({ content }: WikiMarkdownRendererProps) {
  return (
    <div className="prose prose-sm max-w-none dark:prose-invert">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          p: ({ children, ...props }) => {
            // Process children for [[wikilinks]]
            const processed = processChildren(children);
            return <p {...props}>{processed}</p>;
          },
          li: ({ children, ...props }) => {
            const processed = processChildren(children);
            return <li {...props}>{processed}</li>;
          },
          table: ({ children, ...props }) => (
            <div className="overflow-x-auto my-4">
              <table
                className="min-w-full border-collapse border border-border text-sm"
                {...props}
              >
                {children}
              </table>
            </div>
          ),
          thead: ({ children, ...props }) => (
            <thead className="bg-muted" {...props}>
              {children}
            </thead>
          ),
          th: ({ children, ...props }) => (
            <th
              className="border border-border px-3 py-2 text-left font-medium"
              {...props}
            >
              {children}
            </th>
          ),
          td: ({ children, ...props }) => (
            <td className="border border-border px-3 py-2" {...props}>
              {children}
            </td>
          ),
          tr: ({ children, ...props }) => (
            <tr className="even:bg-muted/50" {...props}>
              {children}
            </tr>
          ),
          h1: ({ children, ...props }) => (
            <h1 className="text-2xl font-semibold mt-6 mb-3" {...props}>
              {children}
            </h1>
          ),
          h2: ({ children, ...props }) => (
            <h2 className="text-xl font-semibold mt-5 mb-2" {...props}>
              {children}
            </h2>
          ),
          h3: ({ children, ...props }) => (
            <h3 className="text-lg font-medium mt-4 mb-2" {...props}>
              {children}
            </h3>
          ),
          code: ({ children, className, ...props }) => {
            const isBlock = className?.includes("language-");
            if (isBlock) {
              return (
                <code
                  className="block bg-muted p-3 rounded-md text-sm font-mono overflow-x-auto"
                  {...props}
                >
                  {children}
                </code>
              );
            }
            return (
              <code
                className="bg-muted px-1.5 py-0.5 rounded text-sm font-mono"
                {...props}
              >
                {children}
              </code>
            );
          },
          ul: ({ children, ...props }) => (
            <ul className="list-disc pl-6 my-2 space-y-1" {...props}>
              {children}
            </ul>
          ),
          ol: ({ children, ...props }) => (
            <ol className="list-decimal pl-6 my-2 space-y-1" {...props}>
              {children}
            </ol>
          ),
          blockquote: ({ children, ...props }) => (
            <blockquote
              className="border-l-4 border-border pl-4 italic text-muted-foreground my-3"
              {...props}
            >
              {children}
            </blockquote>
          ),
          a: ({ children, href, ...props }) => (
            <a
              href={href}
              className="text-primary underline underline-offset-2"
              {...props}
            >
              {children}
            </a>
          ),
          strong: ({ children, ...props }) => (
            <strong className="font-semibold" {...props}>
              {children}
            </strong>
          ),
          hr: (props) => <hr className="my-4 border-border" {...props} />,
        }}
      />
    </div>
  );
}

function processChildren(children: React.ReactNode): React.ReactNode {
  if (typeof children === "string") {
    return processWikilinks(children);
  }
  if (Array.isArray(children)) {
    return children.map((child, i) => {
      if (typeof child === "string") {
        const processed = processWikilinks(child);
        return processed.length === 1 ? processed[0] : <span key={i}>{processed}</span>;
      }
      return child;
    });
  }
  return children;
}
