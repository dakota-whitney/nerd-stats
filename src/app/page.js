import Stack from 'react-bootstrap/Stack';

export default function Home(){
  return (
    <Stack gap={3} className="vh-100 d-flex flex-column justify-content-center align-items-center text-center">
      <h1 className="display-1">Statistical analysis of all things nerd</h1>
      <h1 className="display-4">Developed by: Dakota Whitney</h1>
      <h1 className="display-6">Platform: Next.js</h1>
      <h1 className="display-6">Theme: Slate by Bootswatch</h1>
    </Stack>
  );
}
