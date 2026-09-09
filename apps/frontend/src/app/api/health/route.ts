import { NextResponse } from "next/server";


export async function GET() {
    try {
        const response = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL}/health`,
            {
                cache: "no-store",
            },
        );

        if (!response.ok) {
            return NextResponse.json(
                {
                    status: "error",
                    message: "Backend health check failed",
                },
                { status: response.status },
            );
        }

        const data = await response.json();

        return NextResponse.json(data);
    } catch {
        return NextResponse.json(
            {
                status: "error",
                message: "Unable to connect to backend",
            },
            { status: 503 },
        );
    }
}