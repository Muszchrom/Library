export default function Score({score}: {score: number}) {
  return (
    <div>
      {Array.from(Array(Math.floor(score)).keys()).map((sc) => 
        <span key={sc} className="text-sm">⭐</span>
      )}
      {!!(score - Math.floor(score)) && (
        <span className="relative text-sm">
          ⭐
          <div className="absolute top-0 bottom-0 right-0 left-1/2 bg-background"></div>
        </span>
      )}
    </div>
  )
}