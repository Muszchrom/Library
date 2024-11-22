export default function Score({score}: {score: number}) {
  return (
    <span className="text-sm tracking-[-0.2rem]">
      {Array.from(Array(Math.floor(score)).keys()).map((sc) => 
        <span key={sc}>⭐</span>
      )}
      {!!(score - Math.floor(score)) && (
        <span className="relative text-sm">
          ⭐
          <div className="absolute top-0 bottom-0 right-[-1px] left-1/2 bg-background"></div>
        </span>
      )}
    </span>
  )
}