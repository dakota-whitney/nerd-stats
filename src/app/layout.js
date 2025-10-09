import "bootswatch/dist/slate/bootstrap.min.css";
import NavBar from "./navbar";

const navLinks = [
  {name: "Yu-Gi-Oh!", href: "yugioh"},
  {name: "Pokémon", href: "pokemon"}
];

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="h-100">
        <NavBar navLinks={navLinks} />
        {children}
      </body>
    </html>
  );
}
