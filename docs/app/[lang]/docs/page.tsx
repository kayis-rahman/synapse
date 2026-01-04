import { base } from "../../source.config";

export default function Page({ params }: { params: { slug?: string[] } }) {
  const page = base.getPage(params.slug);
  if (!page) {
    return <div>Not Found</div>;
  }

  return (
    <div>
      {page.render()}
    </div>
  );
}
