import { defineDocs, defineConfig } from "fumadocs-mdx/config";

export const docs = defineDocs({
  dir: 'content/content',
  docs: {
    schema: {
      frontmatter: {
        title: {
          type: 'string',
          required: true,
        },
        description: {
          type: 'string',
        },
      },
    },
  },
  meta: {
    dir: 'content',
  },
});

export default defineConfig({
  mdx: {
    lastModifiedTime: 'git',
  },
});
