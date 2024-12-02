import BooksRow from "@/components/books-row";
import CategoryRow from "@/components/category-row";

export default function Home() {
  return (
    <div className="flex flex-col gap-2">
      <BooksRow title="Zawsze najlepsze"/>

      <CategoryRow />

      <BooksRow title="Najlepsze w okolicy"/>

      <BooksRow title="Najlepsze w ostatnim czasie"/>
    </div>
  );
}


