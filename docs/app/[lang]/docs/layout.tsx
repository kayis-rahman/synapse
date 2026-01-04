import type { Metadata } from "next";
import { DocsLayout } from "fumadocs-ui/page";
import { base } from "../../../source.config";

export const metadata: Metadata = {
  title: 'Documentation',
  description: 'Complete SYNAPSE documentation',
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <DocsLayout tree={base}>
      {children}
    </DocsLayout>
  );
}
