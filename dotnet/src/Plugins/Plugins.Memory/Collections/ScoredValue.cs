﻿// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
<<<<<<< HEAD
using System.Diagnostics.CodeAnalysis;

namespace Microsoft.SemanticKernel.Memory;
=======

#pragma warning disable IDE0130 // Namespace does not match folder structure
namespace Microsoft.SemanticKernel.Memory.Collections;
#pragma warning restore IDE0130 // Namespace does not match folder structure
>>>>>>> f5c8882d73157409ff27fb857a432fda2fa6c2a3

/// <summary>
/// Structure for storing data which can be scored.
/// </summary>
/// <typeparam name="T">Data type.</typeparam>
<<<<<<< HEAD
internal readonly struct ScoredValue<T>(T item, double score) : IComparable<ScoredValue<T>>, IEquatable<ScoredValue<T>>
{
    /// <summary>
    /// Gets the value of the scored item.
    /// </summary>
    public T Value { get; } = item;
    /// <summary>
    /// Gets the score of the item.
    /// </summary>
    public double Score { get; } = score;

    /// <summary>
    /// Compares the current instance with another instance of <see cref="ScoredValue{T}"/>.
    /// </summary>
    /// <param name="other">The other instance of <see cref="ScoredValue{T}"/> to compare with.</param>
    /// <returns>A value indicating the relative order of the instances.</returns>
=======
public readonly struct ScoredValue<T> : IComparable<ScoredValue<T>>, IEquatable<ScoredValue<T>>
{
    public ScoredValue(T item, double score)
    {
        this.Value = item;
        this.Score = score;
    }

    public T Value { get; }
    public Score Score { get; }

>>>>>>> f5c8882d73157409ff27fb857a432fda2fa6c2a3
    public int CompareTo(ScoredValue<T> other)
    {
        return this.Score.CompareTo(other.Score);
    }

<<<<<<< HEAD
    /// <summary>
    /// Returns a string representation of the current instance.
    /// </summary>
    /// <returns>A string representation of the current instance.</returns>
=======
>>>>>>> f5c8882d73157409ff27fb857a432fda2fa6c2a3
    public override string ToString()
    {
        return $"{this.Score}, {this.Value}";
    }

<<<<<<< HEAD
    /// <summary>
    /// Converts the score of the current instance to a double.
    /// </summary>
    /// <param name="src">The current instance of <see cref="ScoredValue{T}"/>.</param>
=======
>>>>>>> f5c8882d73157409ff27fb857a432fda2fa6c2a3
    public static explicit operator double(ScoredValue<T> src)
    {
        return src.Score;
    }

<<<<<<< HEAD
    /// <summary>
    /// Converts the value of the current instance to the specified type.
    /// </summary>
    /// <param name="src">The current instance of <see cref="ScoredValue{T}"/>.</param>
=======
>>>>>>> f5c8882d73157409ff27fb857a432fda2fa6c2a3
    public static explicit operator T(ScoredValue<T> src)
    {
        return src.Value;
    }

<<<<<<< HEAD
    /// <summary>
    /// Converts a <see cref="KeyValuePair{TKey, TValue}"/> to a <see cref="ScoredValue{T}"/>.
    /// </summary>
    /// <param name="src">The <see cref="KeyValuePair{TKey, TValue}"/> to convert.</param>
=======
>>>>>>> f5c8882d73157409ff27fb857a432fda2fa6c2a3
    public static implicit operator ScoredValue<T>(KeyValuePair<T, double> src)
    {
        return new ScoredValue<T>(src.Key, src.Value);
    }

<<<<<<< HEAD
    /// <inheritdoc/>
    public override bool Equals([NotNullWhen(true)] object? obj)
=======
    public override bool Equals(object obj)
>>>>>>> f5c8882d73157409ff27fb857a432fda2fa6c2a3
    {
        return (obj is ScoredValue<T> other) && this.Equals(other);
    }

<<<<<<< HEAD
    /// <summary>
    /// Determines whether the current instance is equal to another instance of <see cref="ScoredValue{T}"/>.
    /// </summary>
    /// <param name="other">The other instance of <see cref="ScoredValue{T}"/> to compare with.</param>
    /// <returns>True if the instances are equal, false otherwise.</returns>
    public bool Equals(ScoredValue<T> other)
    {
        return EqualityComparer<T>.Default.Equals(this.Value, other.Value) &&
                this.Score.Equals(other.Score);
    }

    /// <inheritdoc/>
=======
    public bool Equals(ScoredValue<T> other)
    {
        return EqualityComparer<T>.Default.Equals(other.Value) &&
               this.Score.Equals(other.Score);
    }

>>>>>>> f5c8882d73157409ff27fb857a432fda2fa6c2a3
    public override int GetHashCode()
    {
        return HashCode.Combine(this.Value, this.Score);
    }

<<<<<<< HEAD
    /// <summary>
    /// Determines whether two instances of <see cref="ScoredValue{T}"/> are equal.
    /// </summary>
=======
>>>>>>> f5c8882d73157409ff27fb857a432fda2fa6c2a3
    public static bool operator ==(ScoredValue<T> left, ScoredValue<T> right)
    {
        return left.Equals(right);
    }

<<<<<<< HEAD
    /// <summary>
    /// Determines whether two instances of <see cref="ScoredValue{T}"/> are not equal.
    /// </summary>
=======
>>>>>>> f5c8882d73157409ff27fb857a432fda2fa6c2a3
    public static bool operator !=(ScoredValue<T> left, ScoredValue<T> right)
    {
        return !(left == right);
    }

<<<<<<< HEAD
    /// <summary>
    /// Determines whether the left instance of <see cref="ScoredValue{T}"/> is less than the right instance.
    /// </summary>
=======
>>>>>>> f5c8882d73157409ff27fb857a432fda2fa6c2a3
    public static bool operator <(ScoredValue<T> left, ScoredValue<T> right)
    {
        return left.CompareTo(right) < 0;
    }

<<<<<<< HEAD
    /// <summary>
    /// Determines whether the left instance of <see cref="ScoredValue{T}"/> is less than or equal to the right instance.
    /// </summary>
=======
>>>>>>> f5c8882d73157409ff27fb857a432fda2fa6c2a3
    public static bool operator <=(ScoredValue<T> left, ScoredValue<T> right)
    {
        return left.CompareTo(right) <= 0;
    }

<<<<<<< HEAD
    /// <summary>
    /// Determines whether the left instance of <see cref="ScoredValue{T}"/> is greater than the right instance.
    /// </summary>
=======
>>>>>>> f5c8882d73157409ff27fb857a432fda2fa6c2a3
    public static bool operator >(ScoredValue<T> left, ScoredValue<T> right)
    {
        return left.CompareTo(right) > 0;
    }

<<<<<<< HEAD
    /// <summary>
    /// Determines whether the left instance of <see cref="ScoredValue{T}"/> is greater than or equal to the right instance.
    /// </summary>
=======
>>>>>>> f5c8882d73157409ff27fb857a432fda2fa6c2a3
    public static bool operator >=(ScoredValue<T> left, ScoredValue<T> right)
    {
        return left.CompareTo(right) >= 0;
    }

<<<<<<< HEAD
    /// <summary>
    /// Returns the minimum possible value of a <see cref="ScoredValue{T}"/>.
    /// </summary>
    internal static ScoredValue<T> Min()
    {
        return new ScoredValue<T>(default!, double.MinValue);
=======
    internal static ScoredValue<T> Min()
    {
        return new ScoredValue<T>(default!, Score.Min);
>>>>>>> f5c8882d73157409ff27fb857a432fda2fa6c2a3
    }
}
