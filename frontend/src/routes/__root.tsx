import * as React from 'react'
import { Link, Outlet, createRootRoute } from '@tanstack/react-router'
import { TanStackRouterDevtools } from '@tanstack/react-router-devtools'

export const Route = createRootRoute({
  component: RootComponent,
})

function RootComponent() {
  return (
    <>
      <div className="p-2 flex gap-4 text-lg border-b border-gray-200 dark:border-gray-700">
        <Link
          to="/"
          activeProps={{
            className: 'font-bold text-blue-500',
          }}
          activeOptions={{ exact: true }}
        >
          Home
        </Link>
        <Link
          to="/chat"
          activeProps={{
            className: 'font-bold text-blue-500',
          }}
        >
          Chat
        </Link>
        <Link
          to="/about"
          activeProps={{
            className: 'font-bold text-blue-500',
          }}
        >
          About
        </Link>
      </div>
      <Outlet />
      <TanStackRouterDevtools position="bottom-right" />
    </>
  )
}
